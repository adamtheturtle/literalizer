class _clientType { @discardableResult func go(first_value: Any = 0, second_value: Any = 0) -> Any { 0 } }
class _appType { var client = _clientType() }
let app = _appType()
app.client.go(first_value: [1], second_value: ["text"]);
