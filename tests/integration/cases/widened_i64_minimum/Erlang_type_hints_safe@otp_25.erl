-module(fixture_widened_i64_minimum_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        -9223372036854775808,
        5
    ],
    My_data.
