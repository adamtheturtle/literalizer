module Fixture_ordered_map_nested_values_Crystal
extend self
my_data = {
    "ordered" => {
        # ordered entry
        "name" => "Alice",
        "scores" => {
            # score meaning
            1 => "first",
            2 => "second",  # latest score
        },
    },
}
end
