module Fixture_string_with_dollar_brace_crystal
extend self
my_data = [
    "prefix ${HOME} suffix",
    "${interpolated}",
]
end
