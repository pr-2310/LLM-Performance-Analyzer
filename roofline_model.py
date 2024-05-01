def roofline_analyze(bandwidth, max_OPS, OPs, memory_access):
    """
    Perform roofline analysis.

    Args:
        bandwidth (float): Bandwidth in bytes/s.
        max_OPS (float): Maximum operations per second.
        OPs (float): Number of operations.
        memory_access (float): Memory access in bytes.

    Returns:
        tuple: A tuple containing arithmetic intensity, performance, and bound.
            - arithmetic_intensity (float): Arithmetic intensity (OPs/byte).
            - performance (float): Performance (OPs/s).
            - bound (str): The bound limiting the performance ("memory" or "compute").
    """
    if memory_access == 0:
        raise ValueError("Memory access cannot be zero.")

    arithmetic_intensity = OPs / memory_access
    turning_point = max_OPS / bandwidth

    if arithmetic_intensity < turning_point:
        bound = "memory"
        performance = arithmetic_intensity * bandwidth
    else:
        bound = "compute"
        performance = max_OPS

    return arithmetic_intensity, performance, bound