module Fixture_string_nul_before_hex_Crystal
extend self
my_data = {
    "x" => "before\u0000after",
}
end
