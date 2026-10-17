require "json"
module Fixture_elm_wrapped_call_result_Crystal_json_type_json_any_call
extend self
def make_widget(value = nil); 0; end
my_data = JSON.parse(%(make_widget(value: JSON.parse(%(1)))))
end
