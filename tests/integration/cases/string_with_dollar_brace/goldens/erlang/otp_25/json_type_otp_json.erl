-module(fixture_string_with_dollar_brace_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"prefix ${HOME} suffix"/utf8>>,
        <<"${interpolated}"/utf8>>
    ],
    My_data.
