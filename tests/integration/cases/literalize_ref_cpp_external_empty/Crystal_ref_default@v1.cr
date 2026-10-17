module Fixture_literalize_ref_cpp_external_empty_Crystal_ref_default
extend self
def consume_widget(_arg = nil); 0; end
item = [
    1,
    2,
]
my_data = [
    1,
    2,
]
consume_widget(_arg: my_data);
my_data = item
consume_widget(_arg: my_data);
end
