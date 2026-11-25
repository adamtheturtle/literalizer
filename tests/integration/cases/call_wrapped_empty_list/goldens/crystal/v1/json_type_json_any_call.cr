require "json"
module Fixture_call_wrapped_empty_list_Crystal_json_type_json_any_call
extend self
def make_widget(value = nil); 0; end
make_widget(value: JSON.parse(%([])));
end
