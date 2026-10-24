-module(fixture_signed_constructor_arguments_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        -16#2A,
        16#0,
        16#2A,
        -1.25,
        0.0,
        1.25
    ],
    My_data.
