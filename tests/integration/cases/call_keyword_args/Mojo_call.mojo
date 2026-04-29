@fieldwise_init
struct _ThrottlerType(Copyable, Movable):
    fn check[*Ts: AnyType](self, *args: *Ts):
        pass
fn emit[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var throttler = _ThrottlerType()
    emit(throttler.check("user_1", 1000.0))
    emit(throttler.check("user_2", 2000.5))
