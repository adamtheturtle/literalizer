-module(fixture_float_special_values_erlang).
-export([x/0]).
x() ->
    My_data = [
        inf,
        '-inf',
        nan
    ],
    My_data.
