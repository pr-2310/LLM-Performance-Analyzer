from configs.Llama import flashattention_transformer_layer_graph, transformer_layer_graph

def get_model_attribute(model_params, attribute_name):
    return getattr(model_params, attribute_name)

def get_num_attention_heads(model_params):
    return get_model_attribute(model_params, "num_attention_heads")

def get_hidden_size(model_params):
    return get_model_attribute(model_params, "hidden_size")

def get_num_key_value_heads(model_params):
    if get_model_attribute(model_params, "multi_query_attention"):
        return get_model_attribute(model_params, "multi_query_group_num")
    else:
        return get_num_attention_heads(model_params)

def get_num_hidden_layers(model_params):
    return get_model_attribute(model_params, "num_layers")

def get_intermediate_size(model_params):
    return get_model_attribute(model_params, "ffn_hidden_size")

def get_vocab_size(model_params):
    return get_model_attribute(model_params, "padded_vocab_size")

def post_process(model_params, args):
    hidden_size = get_hidden_size(model_params)
    vocab_size = get_vocab_size(model_params)
    layers = []
    
    for stage in ["prefill", "decode"]:
        layers.append({
            'name': 'lm_head',
            'stage': stage,
            'OPs': args['batchsize'] * hidden_size * vocab_size * 1,
            'load_weight': hidden_size * vocab_size * args['w_byte'],
            'load_act': hidden_size * args['a_byte'],
            'store_act': vocab_size * args['a_byte'],
        })
    
    return layers

def get_linear_layers(model_params):
    hidden_size = get_hidden_size(model_params)
    intermediate_size = get_intermediate_size(model_params)
    key_value_heads = get_num_key_value_heads(model_params)
    attention_heads = get_num_attention_heads(model_params)
    
    return {
        "q_proj": [hidden_size, hidden_size],
        "k_proj": [hidden_size, hidden_size * key_value_heads / attention_heads],
        "v_proj": [hidden_size, hidden_size * key_value_heads / attention_heads],
        "out_proj": [hidden_size, hidden_size],
        "gate_proj": [hidden_size, intermediate_size],
        "up_proj": [hidden_size, intermediate_size],
        "down_proj": [intermediate_size, hidden_size]
    }