-module(fixture_nested_mixed_inner_erlang_json_type_otp_json_nested_mixed).
-export([x/0]).
x() ->
    My_data = [
        [1, <<"a"/utf8>>],
        [2, <<"b"/utf8>>]
    ],
    My_data.
