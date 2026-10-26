module Fixture_map_beyond_i64_Crystal_type_hints_safe
extend self
my_data = {
    "a" => 9223372036854775807,
    "b" => 9223372036854775808_i128,
}
end
