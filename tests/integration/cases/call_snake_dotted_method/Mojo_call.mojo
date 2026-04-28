struct _Http_clientType:
    fn __init__(inout self): pass
    def fetch(self, *args: object) -> object: return object()
struct _My_appType:
    var http_client: _Http_clientType
    fn __init__(inout self): self.http_client = _Http_clientType()
def main():
    var my_app = _My_appType()
    my_app.http_client.fetch("hello")
    my_app.http_client.fetch(42)
    my_app.http_client.fetch(True)
