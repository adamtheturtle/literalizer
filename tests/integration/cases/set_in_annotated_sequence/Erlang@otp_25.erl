-module(fixture_set_in_annotated_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        sets:from_list([]),
        sets:from_list([1, 2]),
        []
    ],
    My_data.
