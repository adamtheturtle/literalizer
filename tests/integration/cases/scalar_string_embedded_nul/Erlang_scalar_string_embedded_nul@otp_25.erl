-module(fixture_scalar_string_embedded_nul_erlang_scalar_string_embedded_nul).
-export([x/0]).
x() ->
    My_data = "\x{0}x",
    My_data.
