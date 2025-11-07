from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

def default_retry():
    return retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=1, max=8),
    )
