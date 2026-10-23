module Fixture_literalize_ref_cpp_owned_nul_string_Crystal_ref
extend self
shared = "a\u0000b"
my_data = {
    "value" => shared,
}
end
