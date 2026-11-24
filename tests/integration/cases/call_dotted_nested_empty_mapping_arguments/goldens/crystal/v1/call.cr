module Fixture_call_dotted_nested_empty_mapping_arguments_Crystal_call
extend self
class WorkerType_; def process(values = nil, count = nil); 0; end; end
class ApiType_; def worker; WorkerType_.new; end; end
api = ApiType_.new
api.worker.process(values: [1, {} of String => String], count: 42);
api.worker.process(values: [2, {"x" => "s"}], count: 43);
end
