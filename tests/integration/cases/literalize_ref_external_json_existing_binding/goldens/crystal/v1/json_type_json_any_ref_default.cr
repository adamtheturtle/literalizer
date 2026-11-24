require "json"
module Fixture_literalize_ref_external_json_existing_binding_Crystal_json_type_json_any_ref_default
extend self
def consume_widget(arg_value = nil); 0; end
my_data = JSON.parse(%({
    "a": 0
}))
consume_widget(arg_value: my_data);
my_data = JSON.parse(%({
    "a": 1
}))
consume_widget(arg_value: my_data);
end
