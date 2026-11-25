require "json"
module Fixture_call_scalar_args_Crystal_json_type_json_any_call
extend self
def process(value = nil); 0; end
process(value: JSON.parse(%("hello")));
process(value: JSON.parse(%(42)));
process(value: JSON.parse(%(true)));
end
