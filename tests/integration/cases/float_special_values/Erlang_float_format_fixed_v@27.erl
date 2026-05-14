-module(fixture_float_special_values_erlang_float_format_fixed_v).
-export([x/0]).
x() ->
    My_data = [
        inf,
        '-inf',
        nan
    ],
    My_data.
