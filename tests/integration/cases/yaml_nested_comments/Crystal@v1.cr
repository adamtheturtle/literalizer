module Fixture_yaml_nested_comments_Crystal
extend self
my_data = {
    "a" => {
        # inner note
        "b" => 1,  # inline b
    },
    "list" => [
        1,  # first
        2,  # second
    ],
}
end
