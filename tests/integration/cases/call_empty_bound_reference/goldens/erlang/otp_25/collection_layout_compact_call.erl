-module(fixture_call_empty_bound_reference_erlang_collection_layout_compact_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    Items = [],
    make_widget(Items).
