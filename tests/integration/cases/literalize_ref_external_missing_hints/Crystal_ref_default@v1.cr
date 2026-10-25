module Fixture_literalize_ref_external_missing_hints_Crystal_ref_default
extend self
def consume_widget(arg_value = nil); 0; end
item = [
    1,
    2,
]
my_data = [
    1,
    2,
]
consume_widget(arg_value: my_data);
my_data = item
consume_widget(arg_value: my_data);
end
