-module(fixture_scalar_int_large_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = 16#80000000,
    My_data.
