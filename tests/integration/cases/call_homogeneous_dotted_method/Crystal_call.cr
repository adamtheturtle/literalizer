module Fixture_call_homogeneous_dotted_method_Crystal_call
extend self
class ClientType_; def fetch(value = nil); 0; end; end
class AppType_; def client; ClientType_.new; end; end
app = AppType_.new
app.client.fetch(value: "hello");
app.client.fetch(value: "world");
end
