module Fixture_string_with_dollar_brace_Crystal
extend self
my_data = [
    "prefix ${HOME} suffix",
    "${interpolated}",
]
end
