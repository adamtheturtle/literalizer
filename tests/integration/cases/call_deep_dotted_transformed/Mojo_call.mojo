@fieldwise_init
struct _ClientType(Copyable, Movable):
    def fetch[*Ts: AnyType](self, *args: *Ts):
        pass
@fieldwise_init
struct _AppType(Copyable, Movable):
    var client: _ClientType
def emit[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var app = _AppType(_ClientType())
    emit(app.client.fetch("hello"))
    emit(app.client.fetch(42))
    emit(app.client.fetch(True))
