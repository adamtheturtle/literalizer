module Fixture_json5_surrogate_pair_escape_Crystal
extend self
my_data = {
    "astral" => "😀",
    "mixed" => "a😀b",
    "count" => 2,
    "list" => ["😀", 1],
    "nested" => {"inner" => "😀"},
}
end
