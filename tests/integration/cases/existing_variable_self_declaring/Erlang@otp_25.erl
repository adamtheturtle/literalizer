-module(fixture_existing_variable_self_declaring_erlang).
-export([x/0]).
x() ->
    My_data = 1,
    My_data.
