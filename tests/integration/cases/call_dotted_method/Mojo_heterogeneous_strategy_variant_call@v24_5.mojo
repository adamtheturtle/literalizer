from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
@fieldwise_init
struct _ClientType(Copyable, Movable):
    def fetch(self, payload: Value):
        pass
@fieldwise_init
struct _AppType(Copyable, Movable):
    var client: _ClientType
def main():
    var app = _AppType(_ClientType())
    app.client.fetch(Value(String("hello")))
    app.client.fetch(Value(42))
    app.client.fetch(Value(True))
