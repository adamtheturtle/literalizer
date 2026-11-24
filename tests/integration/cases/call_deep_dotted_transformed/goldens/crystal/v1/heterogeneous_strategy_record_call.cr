module Fixture_call_deep_dotted_transformed_Crystal_heterogeneous_strategy_record_call
extend self
class ClientType_; def fetch(payload = nil); 0; end; end
class AppType_; def client; ClientType_.new; end; end
app = AppType_.new
def emit(_arg = nil); 0; end
emit(app.client.fetch(payload: "hello"));
emit(app.client.fetch(payload: 42));
emit(app.client.fetch(payload: true));
end
