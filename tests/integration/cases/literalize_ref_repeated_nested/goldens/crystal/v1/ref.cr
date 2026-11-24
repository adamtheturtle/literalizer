module Fixture_literalize_ref_repeated_nested_Crystal_ref
extend self
shared = [
    1,
    2,
]
my_data = [
    {"left" => shared, "right" => shared},
]
end
