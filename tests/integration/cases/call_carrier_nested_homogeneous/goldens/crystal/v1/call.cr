module Fixture_call_carrier_nested_homogeneous_Crystal_call
extend self
class ClientType_; def go(first_value = nil, second_value = nil); 0; end; end
class AppType_; def client; ClientType_.new; end; end
app = AppType_.new
app.client.go(first_value: [1], second_value: [2]);
end
