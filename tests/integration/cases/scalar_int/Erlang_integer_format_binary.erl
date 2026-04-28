-module(fixture_scalar_int_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = 2#101010,
    My_data.
