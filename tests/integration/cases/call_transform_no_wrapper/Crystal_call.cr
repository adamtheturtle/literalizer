class ApiType_; def request(*a, **kw); 0; end; end
class ClientType_; def api; ApiType_.new; end; end
client = ClientType_.new
client.api.request(data: "hello");
client.api.request(data: 42);
client.api.request(data: true);
