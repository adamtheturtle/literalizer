module Fixture_call_process_member_Crystal_call
extend self
class ProcessType_; def fetch(data = nil); 0; end; end
class AppType_; def process; ProcessType_.new; end; end
app = AppType_.new
app.process.fetch(data: {"data" => "hello"});
app.process.fetch(data: {"data" => 42});
app.process.fetch(data: {"data" => true});
end
