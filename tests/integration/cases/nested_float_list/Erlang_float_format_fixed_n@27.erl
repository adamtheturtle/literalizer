-module(fixture_nested_float_list_erlang_float_format_fixed_n).
-export([x/0]).
x() ->
    My_data = [
        [1.500000, 2.500000],
        [3.500000, 4.500000]
    ],
    My_data.
