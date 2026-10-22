module Fixture_positional_empty_rows_Crystal_type_hints_safe
extend self
my_data = [
    [[1, "value"], [] of String],
    [[] of String, [2, "other"]],
]
end
