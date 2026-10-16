require "json"
module Fixture_call_nim_empty_bound_reference_Crystal_json_type_json_any_call
extend self
def make_widget(value = nil); 0; end
items = JSON.parse(%([]))
make_widget(value: items);
end
