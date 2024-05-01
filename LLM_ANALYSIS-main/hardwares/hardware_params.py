hardware_params = {
    "nvidia_V100": {
        "bandwidth": 900e9,
        "FP16": 112e12,
        "INT8": 62e12,
        "onchip_buffer": 20480e3,
    },
    "nvidia_A6000": {
        "bandwidth": 768e9,
        "FP16": 309.677e12 / 2,
        "INT8": 309.7e12,
        "onchip_buffer": 21504e3,
    },
    "nvidia_A100": {
        "bandwidth": 1555e9,
        "FP16": 312e12,
        "INT8": 624e12,
        "onchip_buffer": 27648e3,
    },
    "nvidia_A100_40G": {
        "bandwidth": 1555e9,
        "FP16": 312e12,
        "INT8": 624e12,
        "onchip_buffer": 27648e3,
    },
    "nvidia_A100_80G": {
        "bandwidth": 2039e9,
        "FP16": 312e12,
        "INT8": 624e12,
        "onchip_buffer": 27648e3,
    },
    "nvidia_A800_80G_SXM": {
        "bandwidth": 2039e9,
        "FP16": 312e12,
        "INT8": 624e12,
        "onchip_buffer": 27648e3,
    },
    "nvidia_A40": {
        "bandwidth": 696e9,
        "FP16": 149.7e12 / 2,
        "INT8": 299.3e12 / 2,
        "onchip_buffer": 21504e3,
    },
    "nvidia_H100": {
        "bandwidth": 3072e9,
        "FP16": 1979e12 / 2,
        "INT8": 3958e12 / 2,
        "onchip_buffer": 33792e3,
    },
    "nvidia_H100_SXM": {
        "bandwidth": 3072e9,
        "FP16": 1979e12 / 2,
        "INT8": 3958e12 / 2,
        "onchip_buffer": 33792e3,
    },
    "nvidia_H100_PCIe": {
        "bandwidth": 2048e9,
        "FP16": 1513e12 / 2,
        "INT8": 3026e12 / 2,
        "onchip_buffer": 29184e3,
    },
    "nvidia_L40": {
        "bandwidth": 864e9,
        "FP16": 181e12,
        "INT8": 362e12,
        "onchip_buffer": 36352e3,
    },
    "intel_13900k": {
        "bandwidth": 89.6e9,
        "FP16": 8 * 5.4e9 * (512 / 16),
        "onchip_buffer": 36e6,
    },
}