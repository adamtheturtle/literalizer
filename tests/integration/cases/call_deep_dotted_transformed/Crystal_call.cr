class ClientType_; def fetch(*a, **kw); 0; end; end
class AppType_; def client; ClientType_.new; end; end
app = AppType_.new
def emit(*a, **kw); 0; end
emit(app.client.fetch(payload: "hello"));
emit(app.client.fetch(payload: 42));
emit(app.client.fetch(payload: true));
