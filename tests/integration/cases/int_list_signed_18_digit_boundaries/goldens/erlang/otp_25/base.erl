-module(fixture_int_list_signed_18_digit_boundaries_erlang).
-export([x/0]).
x() ->
    My_data = [
        999999999999999999,
        -999999999999999999
    ],
    My_data.
