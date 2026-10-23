-module(fixture_nested_list_of_dicts_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = [
        [
            #{
                "name" => "Alice"
            },
            #{
                "name" => "Bob"
            }
        ],
        [
            #{
                "name" => "Charlie"
            },
            #{
                "name" => "Dave"
            }
        ]
    ],
    My_data.
