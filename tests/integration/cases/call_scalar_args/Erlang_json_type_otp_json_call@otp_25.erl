-module(fixture_call_scalar_args_erlang_json_type_otp_json_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(<<"hello"/utf8>>),
    process(42),
    process(true).
