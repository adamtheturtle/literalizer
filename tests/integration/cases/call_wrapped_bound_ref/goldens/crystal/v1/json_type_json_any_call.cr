require "json"
module Fixture_call_wrapped_bound_ref_Crystal_json_type_json_any_call
extend self
def make_widget(value = nil); 0; end
value = JSON.parse(%(1))
make_widget(value: value);
end
