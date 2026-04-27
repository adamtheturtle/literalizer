-module(fixture_nested_empty_inner_erlang).
-export([x/0]).
x() ->
    My_data = [
        [],
        []
    ],
    My_data.
