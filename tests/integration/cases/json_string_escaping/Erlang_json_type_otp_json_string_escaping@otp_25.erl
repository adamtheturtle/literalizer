-module(fixture_json_string_escaping_erlang_json_type_otp_json_string_escaping).
-export([x/0]).
x() ->
    My_data = #{
        <<"$key"/utf8>> => <<"a\"b\tcé #{world} $ident"/utf8>>,
        <<"trailing multi-byte"/utf8>> => <<"café"/utf8>>
    },
    My_data.
