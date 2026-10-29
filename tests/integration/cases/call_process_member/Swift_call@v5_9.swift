class _processType { @discardableResult func fetch(data: Any = 0) -> Any { 0 } }
class _appType { var process = _processType() }
let app = _appType()
app.process.fetch(data: ["data": "hello"]);
app.process.fetch(data: ["data": 42]);
app.process.fetch(data: ["data": true]);
