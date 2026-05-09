def process[*Ts: AnyType](*args: *Ts):
    pass
@fieldwise_init
struct _TracerType(Copyable, Movable):
    def emit[*Ts: AnyType](self, *args: *Ts):
        pass
def main():
    var tracer = _TracerType()
    tracer.emit(process("hello"))
    tracer.emit(process(42))
    tracer.emit(process(True))
