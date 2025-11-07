from prometheus_client import Counter, Histogram

REQUESTS = Counter("srw_requests_total", "API requests", ["route"])
LATENCY = Histogram("srw_latency_seconds", "Latency", ["route"])
TOKENS_IN = Counter("srw_tokens_in", "Tokens in", ["provider","model"])
TOKENS_OUT = Counter("srw_tokens_out", "Tokens out", ["provider","model"])
