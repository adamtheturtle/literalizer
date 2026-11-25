-module(fixture_long_string_before_list_comma_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"This long string keeps its structural comma beyond the Fortran wrapping window without a safe split."/utf8>>,
        1
    ],
    My_data.
