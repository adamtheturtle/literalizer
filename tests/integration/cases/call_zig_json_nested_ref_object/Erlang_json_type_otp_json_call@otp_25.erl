-module(fixture_call_zig_json_nested_ref_object_erlang_json_type_otp_json_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Shared = [
        1,
        2
    ],
    consume(#{<<"field"/utf8>> => Shared, <<"nested"/utf8>> => [Shared, #{}]}).
