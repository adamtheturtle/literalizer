-module(fixture_int_list_signed_18_digit_boundaries_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        2#110111100000101101101011001110100111011000111111111111111111,
        -2#110111100000101101101011001110100111011000111111111111111111
    ],
    My_data.
