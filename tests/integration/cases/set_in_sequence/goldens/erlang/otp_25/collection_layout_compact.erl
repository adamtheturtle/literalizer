-module(fixture_set_in_sequence_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        sets:from_list(["a", "b"])
    ],
    My_data.
