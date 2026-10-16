require "json"
module Fixture_call_nim_dotted_nonempty_result_binding_Crystal_json_type_json_any_call
extend self
class ThingType_; def go(value = nil); 0; end; end
thing = ThingType_.new
my_data = JSON.parse(%(thing.go(value: JSON.parse(%([1])))))
end
