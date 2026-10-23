-module(fixture_empty_dicts_in_sequence_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        #{},
        #{}
    ],
    My_data.
