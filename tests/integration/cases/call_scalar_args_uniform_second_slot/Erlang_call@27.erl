-module(fixture_call_scalar_args_uniform_second_slot_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    process("hello", "a"),
    process(42, "b"),
    process(true, "c").
