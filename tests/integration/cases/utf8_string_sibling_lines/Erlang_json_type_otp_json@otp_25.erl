-module(fixture_utf8_string_sibling_lines_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"中中中中中中中中中中中中中中中中中中中中"/utf8>>,
        <<"é'é'é'é'é'é'é'é'é'é'"/utf8>>,
        <<"🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"/utf8>>
    ],
    My_data.
