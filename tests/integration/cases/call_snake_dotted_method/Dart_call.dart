class _Http_ClientType { dynamic fetch({dynamic payload}) => null; }
class _My_AppType { final http_client = _Http_ClientType(); }
final my_app = _My_AppType();
my_app.http_client.fetch(payload: "hello");
my_app.http_client.fetch(payload: 42);
my_app.http_client.fetch(payload: true);
