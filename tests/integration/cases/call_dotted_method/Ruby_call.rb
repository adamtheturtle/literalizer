class ClientType; def send(*a, **kw); end; end
class NsType; def client; ClientType.new; end; end
ns = NsType.new
ns.client.send(payload: "hello")
ns.client.send(payload: 42)
ns.client.send(payload: true)
