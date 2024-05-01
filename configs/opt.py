def get_model_attribute(model_params, attribute_name):
    return getattr(model_params, attribute_name)

def get_num_attention_heads(model_params):
    return get_model_attribute(model_params, "num_attention_heads")

def get_hidden_size(model_params):
    return get_model_attribute(model_params, "hidden_size")

def get_num_key_value_heads(model_params):
    return get_num_attention_heads(model_params)

def get_num_hidden_layers(model_params):
    return get_model_attribute(model_params, "num_hidden_layers")

def get_intermediate_size(model_params):
    return get_model_attribute(model_params, "ffn_dim")

def get_vocab_size(model_params):
    return get_model_attribute(model_params, "vocab_size")

def post_process(model_params, args):
    hidden_size = get_hidden_size(model_params)
    vocab_size = get_vocab_size(model_params)

    layers = []
    for stage in ["prefill", "decode"]:
        layers.append({
            'name': 'lm_head',
            'stage': stage,
            'OPs': args['batchsize'] * hidden_size * vocab_size,
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
        "k_proj": [hidden_size, hidden_size * key_value_heads // attention_heads],
        "v_proj": [hidden_size, hidden_size * key_value_heads // attention_heads],
        "out_proj": [hidden_size, hidden_size],
        "gate_proj": [hidden_size, intermediate_size],
        "up_proj": [hidden_size, intermediate_size],
        "down_proj": [intermediate_size, hidden_size],
    }

transformer_layer_graph = {
    "input": [],
    "attn_norm": ["input"],
    "q_proj": ["attn_norm"],
    "k_proj": ["attn_norm"],
    "v_proj": ["attn_norm"],
    "qk_matmul": ["q_proj", "k_proj"],
    "softmax": ["qk_matmul"],
    "sv_matmul": ["softmax", "v_proj"],
    "out_proj": ["sv_matmul"],
    "attn_add": ["input", "out_proj"],
    "mlp_norm": ["attn_add"],
    "up_proj": ["mlp_norm"],
    "mlp_act": ["up_proj"],
    "down_proj": ["mlp_act"],
    "mlp_add": ["attn_add", "down_proj"],
    "output": ["mlp_add"],
}

flashattention_transformer_layer_graph = {
    "input": [],
    "attn_norm": ["input"],
    "q_proj": ["attn_norm"],
    "k_proj": ["attn_norm"],
    "v_proj": ["attn_norm"],
    "fused_attention": ["q_proj", "k_proj", "v_proj"],
    "out_proj": ["fused_attention"],
    "attn_add": ["input", "out_proj"],
    "mlp_norm": ["attn_add"],
    "up_proj": ["mlp_norm"],
    "mlp_act": ["up_proj"],
    "down_proj": ["mlp_act"],
    "mlp_add": ["attn_add", "down_proj"],
    "output": ["mlp_add"],
}