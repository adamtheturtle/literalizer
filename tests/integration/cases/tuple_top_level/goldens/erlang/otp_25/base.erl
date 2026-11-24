-module(fixture_tuple_top_level_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        "email",
        "a@gmail.com",
        100
    ],
    My_data.
