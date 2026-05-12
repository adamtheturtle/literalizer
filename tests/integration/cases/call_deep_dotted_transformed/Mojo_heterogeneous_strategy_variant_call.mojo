from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
@fieldwise_init
struct _ClientType(Copyable, Movable):
    def fetch(self, payload: Value) -> None:
        pass
@fieldwise_init
struct _AppType(Copyable, Movable):
    var client: _ClientType
def emit[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var app = _AppType(_ClientType())
    emit(app.client.fetch(Value(String("hello"))))
    emit(app.client.fetch(Value(42)))
    emit(app.client.fetch(Value(True)))
