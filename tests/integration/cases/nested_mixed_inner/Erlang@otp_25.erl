-module(fixture_nested_mixed_inner_erlang).
-export([x/0]).
x() ->
    My_data = [
        [1, "a"],
        [2, "b"]
    ],
    My_data.
