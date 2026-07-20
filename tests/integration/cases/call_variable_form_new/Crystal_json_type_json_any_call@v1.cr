require "json"
module Fixture_call_variable_form_new_Crystal_json_type_json_any_call
extend self
def make_widget(count = nil); 0; end
my_data = JSON.parse(%(make_widget(count: JSON.parse(%(42)))))
end
