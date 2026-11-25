-module(fixture_scalar_int_negative_large_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = -2#10000000000000000000000000000001,
    My_data.
