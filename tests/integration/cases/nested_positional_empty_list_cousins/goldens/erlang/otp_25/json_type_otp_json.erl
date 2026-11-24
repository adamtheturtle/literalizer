-module(fixture_nested_positional_empty_list_cousins_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        [[], []],
        [[1], [1]]
    ],
    My_data.
