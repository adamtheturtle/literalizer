-module(fixture_julia_integer_boundaries_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        -16#8000000000000000,
        16#8000000000000000
    ],
    My_data.
