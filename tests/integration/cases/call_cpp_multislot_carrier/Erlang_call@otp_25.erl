-module(fixture_call_cpp_multislot_carrier_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    process(1, "hello"),
    process("two", false),
    process(3.5, undefined).
