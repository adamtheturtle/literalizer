require "json"
module Fixture_call_ref_cpp_string_ownership_Crystal_json_type_json_any_call
extend self
def consume(value = nil); 0; end
item = JSON.parse(%("s"))
consume(value: item);
end
