-module(fixture_scalar_int_negative_large_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = -16#80000001,
    My_data.
