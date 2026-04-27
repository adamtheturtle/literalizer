class _clientType { @discardableResult func post(data: Any = 0) -> Any { 0 } }
class _apiType { var client = _clientType() }
class _objType { var api = _apiType() }
let obj = _objType()
obj.api.client.post(data: "hello");
obj.api.client.post(data: 42);
obj.api.client.post(data: true);
