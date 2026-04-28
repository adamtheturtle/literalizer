@fieldwise_init
struct _ClientType(Copyable, Movable):
    fn fetch[*Ts: AnyType](self, *args: *Ts):
        pass
@fieldwise_init
struct _AppType(Copyable, Movable):
    var client: _ClientType
def main():
    var app = _AppType(_ClientType())
    app.client.fetch("hello")
    app.client.fetch(42)
    app.client.fetch(True)
