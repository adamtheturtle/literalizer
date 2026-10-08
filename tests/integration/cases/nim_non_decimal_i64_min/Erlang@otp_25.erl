-module(fixture_nim_non_decimal_i64_min_erlang).
-export([x/0]).
x() ->
    My_data = [
        -9223372036854775808,
        -1,
        9223372036854775807
    ],
    My_data.
