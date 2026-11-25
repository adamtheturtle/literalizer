-module(fixture_scalar_null_erlang).
-export([x/0]).
x() ->
    My_data = undefined,
    My_data.
