struct _ClientType:
    fn __init__(inout self): pass
    def post(self, *args: object) -> object: return object()
struct _ApiType:
    var client: _ClientType
    fn __init__(inout self): self.client = _ClientType()
struct _ObjType:
    var api: _ApiType
    fn __init__(inout self): self.api = _ApiType()
def main():
    var obj = _ObjType()
    obj.api.client.post("hello")
    obj.api.client.post(42)
    obj.api.client.post(True)
