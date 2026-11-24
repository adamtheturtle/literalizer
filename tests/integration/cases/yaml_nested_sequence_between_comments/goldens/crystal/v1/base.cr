module Fixture_yaml_nested_sequence_between_comments_Crystal
extend self
my_data = [
    [
        {"item" => "existing"},
        "kept",
        # This comment trails the first pair.
    ],
    [{"item" => "next"}, "also kept"],
    # This comment describes the last pair.
    [{"item" => "last"}, "kept too"],
]
end
