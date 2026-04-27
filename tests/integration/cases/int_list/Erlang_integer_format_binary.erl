-module(fixture_int_list_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        2#1,
        2#10,
        2#11
    ],
    My_data.
