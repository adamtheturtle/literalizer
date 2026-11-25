-module(fixture_call_ref_external_empty_erlang_collection_layout_compact_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = [
        1,
        2
    ],
    consume(Item).
