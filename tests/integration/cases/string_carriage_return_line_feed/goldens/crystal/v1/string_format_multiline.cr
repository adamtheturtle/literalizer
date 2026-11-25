module Fixture_string_carriage_return_line_feed_Crystal_string_format_multiline
extend self
my_data = {
     %q|cr| => "a\rb",
     %q|crlf| => "a\r\nb",
     %q|lf| => %q|a
b|,
}
end
