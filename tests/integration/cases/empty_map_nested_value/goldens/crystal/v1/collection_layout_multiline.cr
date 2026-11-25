module Fixture_empty_map_nested_value_Crystal_collection_layout_multiline
extend self
my_data = [
    [
        {
            "mapping" => {} of String => String,
        },
        {} of String => String,
    ],
    [
        {} of String => String,
        {
            "mapping" => {} of String => String,
        },
    ],
]
end
