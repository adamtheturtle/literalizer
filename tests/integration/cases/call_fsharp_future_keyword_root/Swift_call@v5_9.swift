class _apiType { @discardableResult func fetch(data: Any = 0) -> Any { 0 } }
class _processType { var api = _apiType() }
let process = _processType()
process.api.fetch(data: ["data": "hello"]);
process.api.fetch(data: ["data": 42]);
process.api.fetch(data: ["data": true]);
