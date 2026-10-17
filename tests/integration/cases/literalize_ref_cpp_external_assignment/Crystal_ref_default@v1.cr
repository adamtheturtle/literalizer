module Fixture_literalize_ref_cpp_external_assignment_Crystal_ref_default
extend self
def consume_widget(_arg = nil); 0; end
ref_data = [
    1,
    2,
]
my_data = [
    0,
]
consume_widget(_arg: my_data);
my_data = ref_data
consume_widget(_arg: my_data);
end
