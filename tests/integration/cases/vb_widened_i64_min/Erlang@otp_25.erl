-module(fixture_vb_widened_i64_min_erlang).
-export([x/0]).
x() ->
    My_data = [
        -9223372036854775808,
        5
    ],
    My_data.
