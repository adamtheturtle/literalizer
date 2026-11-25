-module(fixture_escaped_mapping_keys_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"quote\"backslash\\"/utf8>> => 1,
        <<"line\nbreak"/utf8>> => 2,
        <<"$(literal)${text}"/utf8>> => 3,
        <<"RStr prefix"/utf8>> => 4
    },
    My_data.
