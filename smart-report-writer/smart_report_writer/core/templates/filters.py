def filters():
    return {
        "truncate": lambda s, n=500: (s[:n] + "…") if len(s) > n else s,
        "md_heading": lambda s, level=2: "#"*level + " " + s,
    }
