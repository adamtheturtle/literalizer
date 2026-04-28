module Fixture_call_deep_dotted_method_Crystal_call
extend self
class ClientType_; def post(data = nil); 0; end; end
class ApiType_; def client; ClientType_.new; end; end
class ObjType_; def api; ApiType_.new; end; end
obj = ObjType_.new
obj.api.client.post(data: "hello");
obj.api.client.post(data: 42);
obj.api.client.post(data: true);
end
