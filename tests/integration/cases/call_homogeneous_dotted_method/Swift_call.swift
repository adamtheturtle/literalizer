class _clientType { @discardableResult func fetch(value: Any = 0) -> Any { 0 } }
class _appType { var client = _clientType() }
let app = _appType()
app.client.fetch(value: "hello");
app.client.fetch(value: "world");
