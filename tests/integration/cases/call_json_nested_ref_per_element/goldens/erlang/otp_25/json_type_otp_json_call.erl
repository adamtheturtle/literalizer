-module(fixture_call_json_nested_ref_per_element_erlang_json_type_otp_json_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Shared = [
        1,
        2
    ],
    consume(#{<<"field"/utf8>> => Shared}),
    consume(Shared).
