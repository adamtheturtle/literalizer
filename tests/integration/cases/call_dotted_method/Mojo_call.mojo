struct _ClientType:
    fn __init__(inout self): pass
    def fetch(self, *args: object) -> object: return object()
struct _AppType:
    var client: _ClientType
    fn __init__(inout self): self.client = _ClientType()
def main():
    var app = _AppType()
    app.client.fetch("hello")
    app.client.fetch(42)
    app.client.fetch(True)
