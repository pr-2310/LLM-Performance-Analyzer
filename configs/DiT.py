def get_model_attribute(model_params, attribute_name, default_value=None):
    return getattr(model_params, attribute_name, default_value)

def get_num_attention_heads(model_params):
    return get_model_attribute(model_params, "num_heads")

def get_hidden_size(model_params):
    return get_model_attribute(model_params, "hidden_size")

def get_num_key_value_heads(model_params):
    return get_model_attribute(model_params, "num_heads")

def get_num_hidden_layers(model_params):
    return get_model_attribute(model_params, "depth")

def get_intermediate_size(model_params):
    mlp_ratio = get_model_attribute(model_params, "mlp_ratio", 4.0)
    hidden_size = get_hidden_size(model_params)
    return hidden_size * mlp_ratio

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
        "down_proj": [intermediate_size, hidden_size],
    }

def post_process(model_params, args):
    return []

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