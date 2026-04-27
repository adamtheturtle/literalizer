module Fixture_call_snake_dotted_method_crystal_call
extend self
class HttpClientType_; def fetch(payload = nil); 0; end; end
class MyAppType_; def http_client; HttpClientType_.new; end; end
my_app = MyAppType_.new
my_app.http_client.fetch(payload: "hello");
my_app.http_client.fetch(payload: 42);
my_app.http_client.fetch(payload: true);
end
