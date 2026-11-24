-module(fixture_int_set_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        16#1,
        16#2,
        16#3
    ]),
    My_data.
