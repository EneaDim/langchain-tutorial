import logging, sys, json, os

def setup_logging():
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
