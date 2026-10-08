module Fixture_literalize_ref_cpp_mixed_sibling_maps_Crystal_ref
extend self
actual = 42
my_data = [
    {"$ref" => 1},
    {"$ref" => nil},
    actual,
]
end
