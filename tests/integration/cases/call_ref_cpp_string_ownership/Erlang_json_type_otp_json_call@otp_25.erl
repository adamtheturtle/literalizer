-module(fixture_call_ref_cpp_string_ownership_erlang_json_type_otp_json_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = <<"s"/utf8>>,
    consume(Item).
