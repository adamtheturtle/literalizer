-module(fixture_int_set_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        2#1,
        2#10,
        2#11
    ]),
    My_data.
