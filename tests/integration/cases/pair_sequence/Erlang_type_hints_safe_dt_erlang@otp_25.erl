-module(fixture_pair_sequence_erlang_type_hints_safe_dt_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        "hello"
    ],
    My_data.
