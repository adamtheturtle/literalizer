-module(fixture_tuple_empty_first_sequence_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [],
        [1, "value"],
        [2, "other"]
    ],
    My_data.
