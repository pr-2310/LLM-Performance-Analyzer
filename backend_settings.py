from hardwares.hardware_params import hardware_params

available_model_ids_sources = {
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
    "custom:2835268853104115712": {
        "source": "custom",
        "endpoint_id": "2835268853104115712",
        "project_id": "604007508233",
        "location": "us-central1",
        "model_name": "opt-1.3b"
    },
    "custom:2835268853104115712": {
        "source": "custom",
        "endpoint_id": "2835268853104115712",
        "project_id": "604007508233",
        "location": "us-central1",
        "model_name": "opt-2.7b"
    },
    # Add more custom endpoints as needed
}

available_model_ids = list(available_model_ids_sources.keys())
available_hardwares = list(hardware_params.keys())