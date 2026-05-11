-module(fixture_call_scalar_args_with_null_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(undefined),
    process("hello").
