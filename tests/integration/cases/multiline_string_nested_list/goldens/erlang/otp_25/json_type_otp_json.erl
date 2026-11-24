-module(fixture_multiline_string_nested_list_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        [<<"\nfirst line\n  indented\n\nlast line\n"/utf8>>]
    ],
    My_data.
