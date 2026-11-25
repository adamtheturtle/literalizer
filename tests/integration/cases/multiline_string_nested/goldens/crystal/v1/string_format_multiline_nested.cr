module Fixture_multiline_string_nested_Crystal_string_format_multiline_nested
extend self
my_data = {
     %q|outer| => [[%q|nested first line
  indented

nested last line
|]],
}
end
