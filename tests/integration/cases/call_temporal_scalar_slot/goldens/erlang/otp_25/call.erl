-module(fixture_call_temporal_scalar_slot_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process("09:30:00"),
    process("2024-01-15T00:00:00+00:00"),
    process(1).
