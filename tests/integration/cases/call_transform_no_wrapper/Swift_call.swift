class _apiType { func request(data: Any = 0) -> Any { 0 } }
class _clientType { var api = _apiType() }
let client = _clientType()
client.api.request(data: "hello");
client.api.request(data: 42);
client.api.request(data: true);
