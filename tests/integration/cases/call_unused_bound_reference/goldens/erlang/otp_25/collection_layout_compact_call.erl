-module(fixture_call_unused_bound_reference_erlang_collection_layout_compact_call).
-export([x/0]).
f(_) -> ok.
x() ->
    f([1, 2]).
