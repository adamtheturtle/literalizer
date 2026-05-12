-module(fixture_nested_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = #{
        "users" => [
            #{
                "name" => "Bob",
                "tags" => [
                    "admin",
                    "user"
                ]
            },
            #{
                "name" => "Carol",
                "tags" => [
                    "guest"
                ]
            }
        ]
    },
    My_data.
