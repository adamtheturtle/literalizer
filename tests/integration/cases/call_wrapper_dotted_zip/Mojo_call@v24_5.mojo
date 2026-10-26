def process(value: Int) -> None:
    pass
@fieldwise_init
struct _HelpersType(Copyable, Movable):
    def emit[*Ts: AnyType](self, *args: *Ts):
        pass
def main():
    var helpers = _HelpersType()
    helpers.emit(process(1), 42)
