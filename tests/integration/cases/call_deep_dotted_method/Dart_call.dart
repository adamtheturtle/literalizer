class _ClientType { dynamic post({dynamic data}) => null; }
class _ApiType { final client = _ClientType(); }
class _ObjType { final api = _ApiType(); }
final obj = _ObjType();
obj.api.client.post(data: "hello");
obj.api.client.post(data: 42);
obj.api.client.post(data: true);
