module Check
extend self
class ClientType_; def fetch(payload = nil); 0; end; end
class AppType_; def client; ClientType_.new; end; end
app = AppType_.new
app.client.fetch(payload: "hello");
app.client.fetch(payload: 42);
app.client.fetch(payload: true);
end
