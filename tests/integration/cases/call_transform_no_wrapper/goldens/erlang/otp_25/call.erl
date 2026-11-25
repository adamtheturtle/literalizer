-module(fixture_call_transform_no_wrapper_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process("hello"),
    process(42),
    process(true).
