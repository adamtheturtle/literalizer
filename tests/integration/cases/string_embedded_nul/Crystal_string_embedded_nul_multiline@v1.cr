module Fixture_string_embedded_nul_Crystal_string_embedded_nul_multiline
extend self
my_data = {
     %q|x| => "\x00",
     %q|y| => "\x001",
}
end
