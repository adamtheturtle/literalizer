from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
@fieldwise_init
struct _Http_clientType(Copyable, Movable):
    def fetch(self, payload: Value):
        pass
@fieldwise_init
struct _My_appType(Copyable, Movable):
    var http_client: _Http_clientType
def main():
    var my_app = _My_appType(_Http_clientType())
    my_app.http_client.fetch(Value(String("hello")))
    my_app.http_client.fetch(Value(42))
    my_app.http_client.fetch(Value(True))
