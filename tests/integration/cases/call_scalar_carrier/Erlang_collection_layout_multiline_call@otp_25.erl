-module(fixture_call_scalar_carrier_erlang_collection_layout_multiline_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process("hello"),
    process(42),
    process(true),
    process(undefined).
