import os
import importlib
from hardwares.hardware_params import hardware_params
from roofline_model import roofline_analyze
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
from utils import str_number, str_number_time
import math

ALL_DATA_NAMES = [
    "OPs",
    "memory_access",
    "load_weight",
    "load_act",
    "store_act",
    "load_kv_cache",
    "store_kv_cache",
    "inference_time",
]


class ModelAnalyzer:
    def __init__(self, model_id, hardware, config_file=None, source="huggingface", model_info=None):
        self.model_id = model_id
        self.hardware = hardware
        self.config_file = self._find_config_file(config_file)
        
        if source == "custom":
            self.model_params = model_info
            self.config = importlib.import_module(config_file.replace(".py", ""))
        else:
            self.model_params = self._load_model_params(source)
            self.config = importlib.import_module(
                self.config_file.replace("/", ".").replace(".py", "")
            )
        
        self.results = None
        self.w_bit = None
        self.a_bit = None
        self.kv_bit = None
        self.batchsize = None
        self.seqlen = None

    def _find_config_file(self, config_file):
        if config_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            for file in os.listdir(current_dir + "/configs"):
                if file.endswith(".py") and file.replace(".py", "") in self.model_id:
                    config_file = "configs/" + file
        assert (
            config_file is not None
        ), "config file is not found, please specify it manually."
        print(f"use config file {config_file} for {self.model_id}")
        return config_file

    def _load_model_params(self, source):
        if source == "huggingface":
            return AutoConfig.from_pretrained(self.model_id, trust_remote_code=True)
        elif source == "custom":
            raise ValueError("Custom source type should be handled in the __init__ method.")
        else:
            module = importlib.import_module(f"model_params.{source}")
            return module.model_params[self.model_id]

    def _analyze_to_results(self, stage, name, **kwargs):
        bandwidth, max_OPS, onchip_buffer = self.get_hardware_info()
        memory_access = sum(kwargs.values())
        arithmetic_intensity, performance, bound = roofline_analyze(
            bandwidth, max_OPS, kwargs["OPs"], memory_access
        )
        inference_time = kwargs["OPs"] / performance
        self.results[stage][name] = {
            "OPs": kwargs["OPs"],
            "memory_access": memory_access,
            "arithmetic_intensity": arithmetic_intensity,
            "performance": performance,
            "bound": bound,
            **kwargs,
            "inference_time": inference_time,
        }

    def save_csv(self, save_path=None):
        if save_path is None:
            save_path = f"output/{self.model_id[:self.model_id.rfind('/')]}"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            save_path += f"{self.model_id[self.model_id.rfind('/'):]}"

        decode_file_name = f"{save_path}_decode.csv"
        prefill_file_name = f"{save_path}_prefill.csv"
        print(f"save to {decode_file_name} and {prefill_file_name}")

        for file_name, stage in [
            (decode_file_name, "decode"),
            (prefill_file_name, "prefill"),
        ]:
            with open(file_name, "a+") as f:
                f.write(
                    f"\n\n=== {self.model_id} {self.hardware} w_bit={self.w_bit} a_bit={self.a_bit} kv_bit={self.kv_bit} batchsize={self.batchsize} seqlen={self.seqlen}===\n"
                )
                f.write(
                    f"layer_name,OPs,Access,arithmetic_intensity,performance,bound,load_weight,load_act,store_act,load_kv_cache,store_kv_cache,inference_time\n"
                )
            with open(file_name, "a+") as f:
                for layer_name, result in self.results[stage].items():
                    f.write(
                        f"{layer_name},{str_number(result['OPs'])},{str_number(result['memory_access'])}B,{str_number(result['arithmetic_intensity'])},{str_number(result['performance'])},{result['bound']},{str_number(result['load_weight'])}B,{str_number(result['load_act'])}B,{str_number(result['store_act'])}B,{str_number(result['load_kv_cache'])}B,{str_number(result['store_kv_cache'])}B,{str_number_time(result['inference_time'])}s\n"
                    )

    def analyze(
        self,
        seqlen,
        batchsize,
        w_bit=16,
        a_bit=16,
        kv_bit=None,
        use_flashattention=False,
        kv_token_ratio=1,
    ):
        assert seqlen > 0
        assert batchsize > 0
        self.results = {"decode": {}, "prefill": {}}
        if kv_bit is None:
            kv_bit = a_bit
        self.w_bit = w_bit
        self.a_bit = a_bit
        self.kv_bit = kv_bit
        self.batchsize = batchsize
        self.seqlen = seqlen

        w_byte = self.w_bit / 8
        a_byte = self.a_bit / 8
        kv_byte = self.kv_bit / 8

        config = self.config
        model_params = self.model_params
        num_attention_heads = config.get_num_attention_heads(model_params)
        hidden_size = config.get_hidden_size(model_params)
        num_key_value_heads = config.get_num_key_value_heads(model_params)

        self._analyze_linear_layers(w_byte, a_byte, kv_byte)
        self._analyze_attention(
            w_byte,
            a_byte,
            kv_byte,
            num_attention_heads,
            hidden_size,
            num_key_value_heads,
            use_flashattention,
        )
        self._analyze_norms_and_activations(a_byte, hidden_size)

        num_hidden_layers = config.get_num_hidden_layers(model_params)
        self._compute_total(num_hidden_layers)

        args = {'batchsize': batchsize, 'a_byte': a_byte, 'w_byte': w_byte}
        self._analyze_lm_head(args)

        return self.results

    def _analyze_linear_layers(self, w_byte, a_byte, kv_byte):
        for name, (ic, oc) in self.config.get_linear_layers(self.model_params).items():
            is_kv_proj = name in ["k_proj", "v_proj"]
            is_normal_proj = not is_kv_proj
            self._analyze_to_results(
                "decode",
                name,
                OPs=ic * oc * self.batchsize * 2,
                load_weight=ic * oc * w_byte,
                load_act=ic * self.batchsize * a_byte,
                store_act=0 if is_kv_proj else oc * self.batchsize * a_byte,
                load_kv_cache=0,
                store_kv_cache=(0 if is_normal_proj else oc * self.batchsize * kv_byte),
            )
            self._analyze_to_results(
                "prefill",
                name,
                OPs=ic * oc * self.batchsize * self.seqlen * 2,
                load_weight=ic * oc * w_byte,
                load_act=ic * self.batchsize * self.seqlen * a_byte,
                store_act=(0 if is_kv_proj else oc * self.batchsize * self.seqlen * a_byte),
                load_kv_cache=0,
                store_kv_cache=(
                    0 if is_normal_proj else oc * self.batchsize * self.seqlen * kv_byte
                ),
            )

    def _analyze_attention(
        self,
        w_byte,
        a_byte,
        kv_byte,
        num_attention_heads,
        hidden_size,
        num_key_value_heads,
        use_flashattention,
    ):
        head_size = hidden_size // num_attention_heads
        qk_matmul_OPs = self.seqlen * head_size * num_attention_heads * self.batchsize * 2
        sv_matmul_OPs = (
            1 * head_size * self.seqlen * num_attention_heads * self.batchsize * 2
        )
        softmax_OPs = (
            self.batchsize * num_attention_heads * self.seqlen * 1 * 5
        )

        if use_flashattention:
            self._analyze_flashattention(
                a_byte,
                kv_byte,
                head_size,
                num_attention_heads,
                qk_matmul_OPs,
                sv_matmul_OPs,
                softmax_OPs,
            )
        else:
            self._analyze_qk_matmul(
                a_byte, kv_byte, head_size, num_key_value_heads, qk_matmul_OPs
            )
            self._analyze_sv_matmul(
                a_byte,
                kv_byte,
                head_size,
                num_attention_heads,
                num_key_value_heads,
                sv_matmul_OPs,
            )
            self._analyze_softmax(a_byte, num_attention_heads, softmax_OPs)

    def _analyze_flashattention(
        self,
        a_byte,
        kv_byte,
        head_size,
        num_attention_heads,
        qk_matmul_OPs,
        sv_matmul_OPs,
        softmax_OPs,
    ):
        bandwidth, max_OPS, onchip_buffer = self.get_hardware_info()
        block_size_r = min(
            math.ceil(onchip_buffer / (kv_byte * head_size)), head_size
        )
        n_blocks_r = math.ceil(1 / block_size_r)
        q_numel = (1) * head_size * self.batchsize * num_attention_heads * a_byte
        o_numel = 1 * self.seqlen * self.batchsize * num_attention_heads * a_byte
        self._analyze_to_results(
            "decode",
            "fused_attention",
            OPs=qk_matmul_OPs + sv_matmul_OPs + softmax_OPs,
            load_weight=0,
            load_act=q_numel,
            store_act=o_numel * 2,
            load_kv_cache=n_blocks_r
            * (self.seqlen)
            * head_size
            * self.batchsize
            * num_attention_heads
            * kv_byte,
            store_kv_cache=0,
        )

    def _analyze_qk_matmul(
        self, a_byte, kv_byte, head_size, num_key_value_heads, qk_matmul_OPs
    ):
        self._analyze_to_results(
            "decode",
            "qk_matmul",
            OPs=qk_matmul_OPs,
            load_weight=0,
            load_act=(1) * head_size * self.batchsize * num_key_value_heads * a_byte,
            store_act=1 * self.seqlen * self.batchsize * num_key_value_heads * a_byte,
            load_kv_cache=(self.seqlen)
            * head_size
            * self.batchsize
            * num_key_value_heads
            * kv_byte,
            store_kv_cache=0,
        )

    def _analyze_sv_matmul(
        self,
        a_byte,
        kv_byte,
        head_size,
        num_attention_heads,
        num_key_value_heads,
        sv_matmul_OPs,
    ):
        self._analyze_to_results(
            "decode",
            "sv_matmul",
            OPs=sv_matmul_OPs,
            load_weight=0,
            load_act=(1 * self.seqlen * self.batchsize * num_attention_heads) * a_byte,
            store_act=1 * head_size * self.batchsize * num_attention_heads * a_byte,
            load_kv_cache=(
                self.seqlen * head_size * self.batchsize * num_key_value_heads
            )
            * kv_byte,
            store_kv_cache=0,
        )

    def _analyze_softmax(self, a_byte, num_attention_heads, softmax_OPs):
        self._analyze_to_results(
            "decode",
            "softmax",
            OPs=softmax_OPs,
            load_weight=0,
            load_act=self.batchsize * num_attention_heads * self.seqlen * 1 * a_byte,
            store_act=self.batchsize * num_attention_heads * self.seqlen * 1 * a_byte,
            load_kv_cache=0,
            store_kv_cache=0,
        )

    def _analyze_norms_and_activations(self, a_byte, hidden_size):
        for name in ["attn_norm", "mlp_norm"]:
            self._analyze_to_results(
                "decode",
                name,
                OPs=self.batchsize * hidden_size * 1 * 7,
                load_weight=0,
                load_act=self.batchsize * hidden_size * 1 * a_byte,
                store_act=self.batchsize * hidden_size * 1 * a_byte,
                load_kv_cache=0,
                store_kv_cache=0,
            )

        for name in ["attn_add", "mlp_add"]:
            self._analyze_to_results(
                "decode",
                name,
                OPs=self.batchsize * hidden_size * 1,
                load_weight=0,
                load_act=self.batchsize * hidden_size * 1 * a_byte,
                store_act=self.batchsize * hidden_size * 1 * a_byte,
                load_kv_cache=0,
                store_kv_cache=0,
            )
        for name in ["mlp_act"]:
            self._analyze_to_results(
                "decode",
                name,
                OPs=self.batchsize * hidden_size * 1 * 2,
                load_weight=0,
                load_act=self.batchsize * hidden_size * 1 * a_byte * 2,
                store_act=self.batchsize * hidden_size * 1 * a_byte,
                load_kv_cache=0,
                store_kv_cache=0,
            )

    def _compute_total(self, num_hidden_layers):
        total_results = {"decode": {}, "prefill": {}}
        for data_name in ALL_DATA_NAMES:
            total_results["decode"][data_name] = 0
            total_results["prefill"][data_name] = 0
        for stage in ["decode", "prefill"]:
            for layer_name, result in self.results[stage].items():
                for data_name in ALL_DATA_NAMES:
                    total_results[stage][data_name] += (
                        result[data_name] * num_hidden_layers
                    )

        weight_kv_footprint = (
            total_results["prefill"]["load_weight"]
            + total_results["prefill"]["store_kv_cache"]
        )
        decode_tmp_act = sum(
            result["store_act"] for result in self.results["decode"].values()
        )
        total_results["decode"]["memory_consumption"] = (
            decode_tmp_act + weight_kv_footprint
        )
        total_results["decode"]["memory_consumption_tmp_act"] = decode_tmp_act
        total_results["decode"]["memory_consumption_weight"] = total_results["prefill"][
            "load_weight"
        ]
        total_results["decode"]["memory_consumption_kv_cache"] = total_results[
            "prefill"
        ]["store_kv_cache"]
        prefill_tmp_act = sum(
            result["store_act"] for result in self.results["prefill"].values()
        )
        total_results["prefill"]["memory_consumption"] = (
            prefill_tmp_act + weight_kv_footprint
        )
        total_results["prefill"]["memory_consumption_tmp_act"] = prefill_tmp_act
        total_results["prefill"]["memory_consumption_weight"] = total_results[
            "prefill"
        ]["load_weight"]
        total_results["prefill"]["memory_consumption_kv_cache"] = total_results[
            "prefill"
        ]["store_kv_cache"]

        self.results["total_results"] = total_results

    def _analyze_lm_head(self, args):
        for layer_info in self.config.post_process(self.model_params, args):
            self._analyze_to_results(
                **layer_info)
            for data_name in ALL_DATA_NAMES:
                self.results["total_results"][layer_info['stage']][data_name] += self.results[layer_info['stage']][layer_info['name']][data_name]

    def analyze_generate_task(
        self, prompt_len, gen_len, batchsize, w_bit=16, a_bit=16, kv_bit=None
    ):
        prefill_result = self.analyze(prompt_len, batchsize, w_bit, a_bit, kv_bit)
        inference_time = prefill_result["total_results"]["prefill"]["inference_time"]
        for i in range(prompt_len, prompt_len + gen_len):
            result = self.analyze(i, batchsize, w_bit, a_bit, kv_bit)
            inference_time += result["total_results"]["decode"]["inference_time"]
        return {"inference_time": inference_time}

    def get_hardware_info(self):
        bandwidth = hardware_params[self.hardware]["bandwidth"]
        if self.w_bit <= 8 and self.a_bit <= 8 and self.kv_bit <= 8:
            max_OPS = hardware_params[self.hardware]["INT8"]
        else:
            max_OPS = hardware_params[self.hardware]["FP16"]
        onchip_buffer = hardware_params[self.hardware]["onchip_buffer"]
        return bandwidth, max_OPS, onchip_buffer

    def get_model_info(self):
        if self.config.get_num_attention_heads(
            self.model_params
        ) != self.config.get_num_key_value_heads(self.model_params):
            GQA = True
        else:
            GQA = False

        info = {"GQA": GQA}
        
        if hasattr(self.model_params, "custom_info"):
            info.update(self.model_params.custom_info)
        
        return info