class _clientType { @discardableResult func fetch(payload: Any = 0) -> Any { 0 } }
class _appType { var client = _clientType() }
let app = _appType()
app.client.fetch(payload: "hello");
app.client.fetch(payload: 42);
app.client.fetch(payload: true);
