from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
import importlib
import os
from hardwares.hardware_params import hardware_params
from model_analyzer import ModelAnalyzer
from utils import str_number
import numpy as np
import re
from backend_settings import available_model_ids_sources

config_cache = {}


def get_analyzer(model_id, hardware, config_path) -> ModelAnalyzer:
    config = f"{model_id}_{hardware}_{config_path}"
    if config not in config_cache:
        config_cache[config] = ModelAnalyzer(
            model_id,
            hardware,
            config_path,
            source=available_model_ids_sources[model_id]["source"],
        )
    return config_cache[config]


def get_quant_bit(dtype):
    if dtype in ["FP16", "INT8"]:
        return {"FP16": 16, "INT8": 8}[dtype]
    elif "bit" in dtype:
        return int(re.findall(r"\d+", dtype)[0])
    else:
        raise ValueError(f"Unsupported dtype: {dtype}")


def analyze_model(model_id, hardware, config_path, inference_config):
    w_bit = get_quant_bit(inference_config["w_quant"])
    a_bit = get_quant_bit(inference_config["a_quant"])
    kv_bit = get_quant_bit(inference_config["kv_quant"])
    seq_length = int(inference_config["seq_length"])
    batch_size = int(inference_config["batch_size"])
    use_flashattention = bool(inference_config["use_flashattention"])
    gen_length = int(inference_config["gen_length"])

    analyzer = get_analyzer(model_id, hardware, config_path)
    result = analyzer.analyze(
        seqlen=seq_length,
        batchsize=batch_size,
        w_bit=w_bit,
        a_bit=a_bit,
        kv_bit=kv_bit,
        use_flashattention=use_flashattention,
    )
    return analyzer, result


def get_hardware_info(analyzer):
    bandwidth, max_OPS, onchip_buffer = analyzer.get_hardware_info()
    return {
        "bandwidth": bandwidth,
        "max_OPS": max_OPS,
        "onchip_buffer": onchip_buffer,
    }


def get_model_info(analyzer):
    return {"GQA": analyzer.get_model_info()["GQA"]}


def write_to_node(nodes, edges, name, OPs, memory_access, info, input_names=[], GQA=False):
    node = {
        "label": name + ("(GQA)" if GQA and name in ["qk_matmul", "sv_matmul"] else ""),
        "id": name,
        "description": f"OPs: {str_number(OPs)}, Access: {str_number(memory_access)}",
        "info": info,
    }
    nodes.append(node)
    for input_name in input_names:
        edge = {"source": input_name, "target": name}
        edges.append(edge)


def analyze_chat_stage(analyzer, result, seq_length, gen_length, batch_size, w_bit, a_bit, kv_bit, use_flashattention):
    total_results = result["total_results"]
    total_results["chat"] = total_results["prefill"]
    n_divide = min(10, gen_length)
    
    for lengthi in np.linspace(seq_length + 1, seq_length + gen_length, n_divide):
        gen_result = analyzer.analyze(
            seqlen=lengthi,
            batchsize=batch_size,
            w_bit=w_bit,
            a_bit=a_bit,
            kv_bit=kv_bit,
            use_flashattention=use_flashattention,
        )
        for k, v in gen_result["total_results"]["decode"].items():
            total_results["chat"][k] += v * gen_length / n_divide
        for name, input_names in analyzer.config.transformer_layer_graph.items():
            if name in gen_result["decode"]:
                result["prefill"][name]["OPs"] += (
                    gen_result["decode"][name]["OPs"] * gen_length / n_divide
                )
                result["prefill"][name]["memory_access"] += (
                    gen_result["decode"][name]["memory_access"] * gen_length / n_divide
                )
    return result, total_results


def get_model_graph(model_id, hardware, config_path, inference_config):
    analyzer, result = analyze_model(model_id, hardware, config_path, inference_config)
    hardware_info = get_hardware_info(analyzer)
    model_info = get_model_info(analyzer)
    GQA = model_info["GQA"]

    nodes = [{"label": "input", "id": "input"}]
    edges = []

    if inference_config["use_flashattention"]:
        layer_graph = analyzer.config.flashattention_transformer_layer_graph
    else:
        layer_graph = analyzer.config.transformer_layer_graph

    stage = inference_config["stage"]
    total_results = result["total_results"]

    if stage != "chat":
        result = result[stage]
    else:
        result, total_results = analyze_chat_stage(
            analyzer, result, int(inference_config["seq_length"]), int(inference_config["gen_length"]),
            int(inference_config["batch_size"]), get_quant_bit(inference_config["w_quant"]),
            get_quant_bit(inference_config["a_quant"]), get_quant_bit(inference_config["kv_quant"]),
            bool(inference_config["use_flashattention"])
        )
        result = result["prefill"]

    for name, input_names in layer_graph.items():
        if name in ["input", "output"]:
            OPs = memory_access = 0
            info = {}
        else:
            OPs = result[name]["OPs"]
            memory_access = result[name]["memory_access"]
            info = result[name]
        write_to_node(nodes, edges, name, OPs, memory_access, info, input_names, GQA)

    return nodes, edges, total_results, hardware_info