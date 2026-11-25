-module(fixture_set_in_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        sets:from_list(["a", "b"])
    ],
    My_data.
