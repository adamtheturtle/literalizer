-module(fixture_int_list_single_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        16#1
    ],
    My_data.
