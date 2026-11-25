module Fixture_call_process_root_Crystal_call
extend self
class ApiType_; def fetch(data = nil); 0; end; end
class ProcessType_; def api; ApiType_.new; end; end
process = ProcessType_.new
process.api.fetch(data: {"data" => "hello"});
process.api.fetch(data: {"data" => 42});
process.api.fetch(data: {"data" => true});
end
