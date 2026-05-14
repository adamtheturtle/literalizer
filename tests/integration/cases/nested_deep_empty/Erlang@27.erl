-module(fixture_nested_deep_empty_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[], []]
    ],
    My_data.
