-module(fixture_mixed_number_list_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = [
        1,
        2.500000,
        3
    ],
    My_data.
