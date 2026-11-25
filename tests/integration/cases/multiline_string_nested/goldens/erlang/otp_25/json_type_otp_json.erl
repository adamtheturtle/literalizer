-module(fixture_multiline_string_nested_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"outer"/utf8>> => [[<<"nested first line\n  indented\n\nnested last line\n"/utf8>>]]
    },
    My_data.
