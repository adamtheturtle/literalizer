-module(fixture_tuple_top_level_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        16#1,
        "email",
        "a@gmail.com",
        16#64
    ],
    My_data.
