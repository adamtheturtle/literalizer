-module(fixture_call_empty_statement_erlang_collection_layout_compact_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    make_widget([]).
