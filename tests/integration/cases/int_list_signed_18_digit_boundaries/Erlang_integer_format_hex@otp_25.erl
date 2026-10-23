-module(fixture_int_list_signed_18_digit_boundaries_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        16#DE0B6B3A763FFFF,
        -16#DE0B6B3A763FFFF
    ],
    My_data.
