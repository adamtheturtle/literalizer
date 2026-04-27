-module(fixture_scalar_int_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = 16#2A,
    My_data.
