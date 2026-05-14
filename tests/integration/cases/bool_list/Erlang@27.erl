-module(fixture_bool_list_erlang).
-export([x/0]).
x() ->
    My_data = [
        true,
        false,
        true
    ],
    My_data.
