module Fixture_positional_empty_map_rows_Crystal
extend self
my_data = {
    "first" => [[1, "value"], [] of String],
    "second" => [[] of String, [2, "other"]],
}
end
