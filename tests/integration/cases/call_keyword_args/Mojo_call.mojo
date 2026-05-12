@fieldwise_init
struct _ThrottlerType(Copyable, Movable):
    def check(self, user_id: String, ts: Float64) -> None:
        pass
def emit[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var throttler = _ThrottlerType()
    emit(throttler.check("user_1", 1000.0))
    emit(throttler.check("user_2", 2000.5))
