module Fixture_yaml_sequence_between_comments_Crystal
extend self
my_data = [
    {"item" => "existing"},
    # This comment describes the next item.
    {"item" => "next"},
]
end
