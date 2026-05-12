@fieldwise_init
struct _ClientType(Copyable, Movable):
    def fetch(self, value: String):
        pass
@fieldwise_init
struct _AppType(Copyable, Movable):
    var client: _ClientType
def main():
    var app = _AppType(_ClientType())
    app.client.fetch("hello")
    app.client.fetch("world")
