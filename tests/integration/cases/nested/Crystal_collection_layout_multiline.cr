module Fixture_nested_Crystal_collection_layout_multiline
extend self
my_data = {
    "users" => [
        {
            "name" => "Bob",
            "tags" => [
                "admin",
                "user",
            ],
        },
        {
            "name" => "Carol",
            "tags" => [
                "guest",
            ],
        },
    ],
}
end
