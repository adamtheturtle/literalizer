-module(fixture_string_carriage_return_line_feed_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"cr"/utf8>> => <<"a\rb"/utf8>>,
        <<"crlf"/utf8>> => <<"a\r\nb"/utf8>>,
        <<"lf"/utf8>> => <<"a\nb"/utf8>>
    },
    My_data.
