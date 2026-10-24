-module(fixture_mixed_number_set_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        2.500000,
        1
    ]),
    My_data.
