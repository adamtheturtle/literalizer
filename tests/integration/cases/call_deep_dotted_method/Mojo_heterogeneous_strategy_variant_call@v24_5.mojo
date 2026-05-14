from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
@fieldwise_init
struct _ClientType(Copyable, Movable):
    def post(self, data: Value):
        pass
@fieldwise_init
struct _ApiType(Copyable, Movable):
    var client: _ClientType
@fieldwise_init
struct _ObjType(Copyable, Movable):
    var api: _ApiType
def main():
    var obj = _ObjType(_ApiType(_ClientType()))
    obj.api.client.post(Value(String("hello")))
    obj.api.client.post(Value(42))
    obj.api.client.post(Value(True))
