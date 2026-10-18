-module(fixture_scalar_int_i64_min_erlang_i64_min_integer_format_binary).
-export([x/0]).
x() ->
    My_data = -2#1000000000000000000000000000000000000000000000000000000000000000,
    My_data.
