module Fixture_deep_cousin_empty_map_Crystal_collection_layout_multiline
extend self
my_data = [
    {
        "outer" => {
            "inner" => {
                "x" => 1,
            },
        },
    },
    {
        "outer" => {
            "inner" => {} of String => String,
        },
    },
]
end
