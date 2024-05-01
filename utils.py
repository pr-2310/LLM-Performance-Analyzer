def format_number(num, unit):
    if num >= 1:
        return f"{num:.1f}"
    else:
        return f"{num:.2f}"

def get_scale_and_unit(num):
    scales = [
        (1e12, "T"),
        (1e9, "G"),
        (1e6, "M"),
        (1e3, "K"),
        (1, "")
    ]

    for scale, unit in scales:
        if num >= scale:
            return scale, unit

    return 1, ""

def str_number(num):
    scale, unit = get_scale_and_unit(num)
    scaled_num = num / scale

    if scaled_num >= 100:
        return f"{scaled_num:.0f}{unit}"
    else:
        return f"{scaled_num:.1f}{unit}"

def str_number_time(num):
    if num >= 1:
        return f"{num:.1f}"
    else:
        scales = [
            (1e-3, "m"),
            (1e-6, "u"),
            (1e-9, "n")
        ]

        for scale, unit in scales:
            if num >= scale:
                return f"{num/scale:.1f}{unit}"

        return f"{num:.0f}"