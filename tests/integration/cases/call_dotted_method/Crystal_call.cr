class ClientType_; def send(*a, **kw); 0; end; end
class NsType_; def client; ClientType_.new; end; end
ns = NsType_.new
ns.client.send(payload: "hello");
ns.client.send(payload: 42);
ns.client.send(payload: true);
