from hardwares.hardware_params import hardware_params

available_model_ids_sources = {
    "meta-llama/Llama-2-7b-hf": {"source": "huggingface"},
    "meta-llama/Llama-2-13b-hf": {"source": "huggingface"},
    "meta-llama/Llama-2-70b-hf": {"source": "huggingface"},
    "THUDM/chatglm3-6b": {"source": "huggingface"},
    "facebook/opt-125m": {"source": "huggingface"},
    "facebook/opt-1.3b": {"source": "huggingface"},
    "facebook/opt-2.7b": {"source": "huggingface"},
    "facebook/opt-6.7b": {"source": "huggingface"},
    "facebook/opt-30b": {"source": "huggingface"},
    "facebook/opt-66b": {"source": "huggingface"},
    "DiT-XL/2": {"source": "DiT"},
    "DiT-XL/4": {"source": "DiT"},
    "custom:2835268853104115712": {
        "source": "custom",
        "endpoint_id": "2835268853104115712",
        "project_id": "604007508233",
        "location": "us-central1",
        "model_name": "opt-125M"
    },
    "custom:12345678901234567": {
        "source": "custom",
        "endpoint_id": "12345678901234567",
        "project_id": "604007508233",
        "location": "us-central1",
        "model_name": "LLAMA-2-7b"
    },
    "custom:98765432109876543": {
        "source": "custom",
        "endpoint_id": "98765432109876543",
        "project_id": "604007508233",
        "location": "us-central1",
        "model_name": "LLAMA-2-13b"
    },
    # Add more custom endpoints as needed
}

available_model_ids = list(available_model_ids_sources.keys())
available_hardwares = list(hardware_params.keys())