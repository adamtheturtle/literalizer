-module(fixture_signed_constructor_arguments_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        -2#101010,
        2#0,
        2#101010,
        -1.25,
        0.0,
        1.25
    ],
    My_data.
