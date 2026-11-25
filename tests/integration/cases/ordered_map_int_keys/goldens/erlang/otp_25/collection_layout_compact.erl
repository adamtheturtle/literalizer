-module(fixture_ordered_map_int_keys_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        {1, "one"},
        {2, "two"},
        {42, "answer"}
    ],
    My_data.
