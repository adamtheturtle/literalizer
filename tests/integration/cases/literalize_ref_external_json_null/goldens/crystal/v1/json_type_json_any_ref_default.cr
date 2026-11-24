require "json"
module Fixture_literalize_ref_external_json_null_Crystal_json_type_json_any_ref_default
extend self
def consume_widget(arg_value = nil); 0; end
item = JSON.parse(%(null))
my_data = JSON.parse(%(null))
consume_widget(arg_value: my_data);
my_data = item
consume_widget(arg_value: my_data);
end
