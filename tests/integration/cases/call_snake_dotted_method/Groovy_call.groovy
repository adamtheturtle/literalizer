class _Http_ClientType { def fetch(Map _args) { null } }
class _My_AppType { def http_client = new _Http_ClientType() }
def my_app = new _My_AppType()
my_app.http_client.fetch(payload: "hello")
my_app.http_client.fetch(payload: 42)
my_app.http_client.fetch(payload: true)
