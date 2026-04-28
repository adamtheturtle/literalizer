-module(fixture_nested_float_list_erlang_float_format_scientific_n).
-export([x/0]).
x() ->
    My_data = [
        [1.5, 2.5],
        [3.5, 4.5]
    ],
    My_data.
