-module(fixture_float_fixed_small_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        1.0e-09,
        -1.0e-09
    },
    My_data.
