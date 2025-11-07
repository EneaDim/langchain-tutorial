class SRWError(Exception):
    pass

class ValidationError(SRWError):
    pass

class UnsupportedError(SRWError):
    pass
