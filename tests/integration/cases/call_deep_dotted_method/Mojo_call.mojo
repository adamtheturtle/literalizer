@fieldwise_init
struct _ClientType(Copyable, Movable):
    fn post[*Ts: AnyType](self, *args: *Ts):
        pass
@fieldwise_init
struct _ApiType(Copyable, Movable):
    var client: _ClientType
@fieldwise_init
struct _ObjType(Copyable, Movable):
    var api: _ApiType
def main():
    var obj = _ObjType(_ApiType(_ClientType()))
    obj.api.client.post("hello")
    obj.api.client.post(42)
    obj.api.client.post(True)
