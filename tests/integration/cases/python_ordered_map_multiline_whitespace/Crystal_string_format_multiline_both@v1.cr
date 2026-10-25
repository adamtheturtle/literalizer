module Fixture_python_ordered_map_multiline_whitespace_Crystal_string_format_multiline_both
extend self
my_data = {
     %q|  leading
key  | => %q|  leading
value
  |,
     %q|next
	key| => [%q|
first
|, %q| last
 |],
}
my_data = {
     %q|  leading
key  | => %q|  leading
value
  |,
     %q|next
	key| => [%q|
first
|, %q| last
 |],
}
end
