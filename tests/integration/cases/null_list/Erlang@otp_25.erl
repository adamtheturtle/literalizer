-module(fixture_null_list_erlang).
-export([x/0]).
x() ->
    My_data = [
        undefined,
        undefined
    ],
    My_data.
