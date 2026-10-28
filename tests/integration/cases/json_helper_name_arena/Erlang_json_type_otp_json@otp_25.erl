-module(fixture_json_helper_name_arena_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    Arena = #{
        <<"a"/utf8>> => 1
    },
    Arena.
