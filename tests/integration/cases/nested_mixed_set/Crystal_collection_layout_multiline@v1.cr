require "set"
module Fixture_nested_mixed_set_Crystal_collection_layout_multiline
extend self
my_data = {
    "name" => "Alice",
    "tags" => Set{
        true,
        42,
        "apple",
    },
}
end
