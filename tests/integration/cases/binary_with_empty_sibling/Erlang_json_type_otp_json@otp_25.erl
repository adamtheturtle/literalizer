-module(fixture_binary_with_empty_sibling_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"SGVsbG8="/utf8>>,
        []
    ],
    My_data.
