from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
def process(value: Value) -> None:
    pass
@fieldwise_init
struct _TracerType(Copyable, Movable):
    def emit[*Ts: AnyType](self, *args: *Ts):
        pass
def main():
    var tracer = _TracerType()
    tracer.emit(process(Value(String("hello"))))
    tracer.emit(process(Value(42)))
    tracer.emit(process(Value(True)))
