-module(fixture_call_ref_null_argument_erlang_collection_layout_compact_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Value = undefined,
    consume(Value).
