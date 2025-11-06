import logging, sys

def setup_logging():
    log = logging.getLogger()
    if log.handlers:
        return
    log.setLevel(logging.INFO)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    log.addHandler(h)

setup_logging()
