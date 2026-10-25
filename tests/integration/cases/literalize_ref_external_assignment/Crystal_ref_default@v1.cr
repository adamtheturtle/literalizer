module Fixture_literalize_ref_external_assignment_Crystal_ref_default
extend self
def consume_widget(arg_value = nil); 0; end
ref_data = [
    1,
    2,
]
my_data = [
    0,
]
consume_widget(arg_value: my_data);
my_data = ref_data
consume_widget(arg_value: my_data);
end
