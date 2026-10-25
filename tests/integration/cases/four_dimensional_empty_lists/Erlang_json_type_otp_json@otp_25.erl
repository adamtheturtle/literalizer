-module(fixture_four_dimensional_empty_lists_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        [[[]]],
        [[[]]]
    ],
    My_data.
