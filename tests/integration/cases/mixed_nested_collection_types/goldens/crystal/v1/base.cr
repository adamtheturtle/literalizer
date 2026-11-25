module Fixture_mixed_nested_collection_types_Crystal
extend self
my_data = {
    "lists" => [[1], ["x"], [] of Int32],
    "maps" => [{"x" => 1}, {"x" => "s"}],
    "empties" => {"a" => [1], "b" => [] of Int32},
}
end
