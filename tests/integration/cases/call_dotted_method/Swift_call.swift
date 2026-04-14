class _clientType { func send(payload: Any = 0) -> Any { 0 } }
class _nsType { var client = _clientType() }
let ns = _nsType()
ns.client.send(payload: "hello");
ns.client.send(payload: 42);
ns.client.send(payload: true);
