-module(fixture_scalar_int_i64_min_erlang_i64_min_integer_format_hex).
-export([x/0]).
x() ->
    My_data = -16#8000000000000000,
    My_data.
