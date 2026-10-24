-module(fixture_tuple_top_level_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        2#1,
        "email",
        "a@gmail.com",
        2#1100100
    ],
    My_data.
