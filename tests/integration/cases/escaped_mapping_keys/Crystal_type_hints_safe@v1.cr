module Fixture_escaped_mapping_keys_Crystal_type_hints_safe
extend self
my_data = {
    "quote\"backslash\\" => 1,
    "line\nbreak" => 2,
    "$(literal)${text}" => 3,
    "RStr prefix" => 4,
}
end
