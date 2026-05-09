@fieldwise_init
struct _Http_clientType(Copyable, Movable):
    def fetch[*Ts: AnyType](self, *args: *Ts):
        pass
@fieldwise_init
struct _My_appType(Copyable, Movable):
    var http_client: _Http_clientType
def main():
    var my_app = _My_appType(_Http_clientType())
    my_app.http_client.fetch("hello")
    my_app.http_client.fetch(42)
    my_app.http_client.fetch(True)
