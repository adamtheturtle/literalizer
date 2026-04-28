struct _ThrottlerType:
    fn __init__(inout self): pass
    def check(self, *args: object) -> object: return object()
def main():
    var throttler = _ThrottlerType()
    def emit(*args: object) -> object: return object()
    emit(throttler.check("user_1", 1000.0))
    emit(throttler.check("user_2", 2000.5))
