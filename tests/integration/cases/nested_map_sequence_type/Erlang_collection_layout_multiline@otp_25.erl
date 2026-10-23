-module(fixture_nested_map_sequence_type_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{
            "b" => [
                1,
                2,
                3
            ]
        }
    },
    My_data.
