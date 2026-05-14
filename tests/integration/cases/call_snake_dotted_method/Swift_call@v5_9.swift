class _http_clientType { @discardableResult func fetch(payload: Any = 0) -> Any { 0 } }
class _my_appType { var http_client = _http_clientType() }
let my_app = _my_appType()
my_app.http_client.fetch(payload: "hello");
my_app.http_client.fetch(payload: 42);
my_app.http_client.fetch(payload: true);
