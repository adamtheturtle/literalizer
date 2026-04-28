class _clientType { @discardableResult func fetch(payload: Any = 0) -> Any { 0 } }
class _appType { var client = _clientType() }
let app = _appType()
@discardableResult func emit(_ _arg: Any = 0) -> Any { 0 }
emit(app.client.fetch(payload: "hello"));
emit(app.client.fetch(payload: 42));
emit(app.client.fetch(payload: true));
