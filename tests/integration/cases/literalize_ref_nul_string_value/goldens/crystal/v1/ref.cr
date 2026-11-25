module Fixture_literalize_ref_nul_string_value_Crystal_ref
extend self
shared = "a\u0000b"
my_data = {
    "value" => shared,
}
end
