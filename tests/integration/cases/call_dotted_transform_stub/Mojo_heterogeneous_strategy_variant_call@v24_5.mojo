from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
def process(var value: Value) -> None:
    pass
@fieldwise_init
struct _TracerType(Copyable, Movable):
    def emit[*Ts: Movable](self, var *args: *Ts):
        pass
def main():
    var tracer = _TracerType()
    tracer.emit(process(Value(String("hello"))))
    tracer.emit(process(Value(42)))
    tracer.emit(process(Value(True)))
