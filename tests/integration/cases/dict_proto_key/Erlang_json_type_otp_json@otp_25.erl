-module(fixture_dict_proto_key_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"__proto__"/utf8>> => #{<<"x"/utf8>> => 1},
        <<"n"/utf8>> => #{<<"__proto__"/utf8>> => 3},
        <<"y"/utf8>> => 2
    },
    My_data.
