-module(fixture_nested_deep_mixed_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[1, 2], ["a", "b"]]
    ],
    My_data.
