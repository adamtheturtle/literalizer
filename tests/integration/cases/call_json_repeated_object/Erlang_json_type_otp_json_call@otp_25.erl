-module(fixture_call_json_repeated_object_erlang_json_type_otp_json_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Shared = #{
        <<"value"/utf8>> => [1, 2]
    },
    consume(#{<<"left"/utf8>> => Shared, <<"right"/utf8>> => Shared}).
