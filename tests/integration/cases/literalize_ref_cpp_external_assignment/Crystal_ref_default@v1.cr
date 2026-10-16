module Fixture_literalize_ref_cpp_external_assignment_Crystal_ref_default
extend self
ref_data = [
    1,
    2,
]
my_data = [
    0,
]
(void)my_data;
my_data = ref_data
(void)my_data;
end
