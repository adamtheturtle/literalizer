-module(fixture_float_list_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = [
        1.100000,
        -2.200000,
        3.300000
    ],
    My_data.
