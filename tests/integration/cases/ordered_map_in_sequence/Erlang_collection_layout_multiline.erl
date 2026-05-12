-module(fixture_ordered_map_in_sequence_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = [
        [
            {"a", 1}
        ],
        "hello"
    ],
    My_data.
