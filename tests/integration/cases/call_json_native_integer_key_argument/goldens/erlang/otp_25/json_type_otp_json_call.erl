-module(fixture_call_json_native_integer_key_argument_erlang_json_type_otp_json_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(#{1 => <<"one"/utf8>>}).
