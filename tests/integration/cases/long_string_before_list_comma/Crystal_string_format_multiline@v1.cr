module Fixture_long_string_before_list_comma_Crystal_string_format_multiline
extend self
my_data = [
    %q|This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.|,
    1,
]
end
