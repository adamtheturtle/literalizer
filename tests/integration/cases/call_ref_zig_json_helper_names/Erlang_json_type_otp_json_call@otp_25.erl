-module(fixture_call_ref_zig_json_helper_names_erlang_json_type_otp_json_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Arena = #{
        <<"a"/utf8>> => 1
    },
    ZVal = #{
        <<"a"/utf8>> => 1
    },
    ZKV = #{
        <<"a"/utf8>> => 1
    },
    process(Arena),
    process(ZVal),
    process(ZKV).
