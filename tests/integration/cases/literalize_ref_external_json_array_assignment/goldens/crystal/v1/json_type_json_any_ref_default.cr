require "json"
module Fixture_literalize_ref_external_json_array_assignment_Crystal_json_type_json_any_ref_default
extend self
def consume_widget(arg_value = nil); 0; end
shared = JSON.parse(%([
    1,
    2
]))
my_data = JSON.parse(%([
    0
]))
consume_widget(arg_value: my_data);
my_data = shared
consume_widget(arg_value: my_data);
end
