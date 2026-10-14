-module(fixture_call_csharp_json_repeated_null_erlang_json_type_otp_json_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Shared = null,
    consume(#{<<"left"/utf8>> => Shared, <<"nested"/utf8>> => [Shared]}).
