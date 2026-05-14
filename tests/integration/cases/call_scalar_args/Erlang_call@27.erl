-module(fixture_call_scalar_args_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process("hello"),
    process(42),
    process(true).
