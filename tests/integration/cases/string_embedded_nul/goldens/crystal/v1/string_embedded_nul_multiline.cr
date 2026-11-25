module Fixture_string_embedded_nul_Crystal_string_embedded_nul_multiline
extend self
my_data = {
     %q|x| => "\u0000",
     %q|y| => "\u00001",
}
end
