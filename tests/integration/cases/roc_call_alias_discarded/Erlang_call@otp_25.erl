-module(fixture_roc_call_alias_discarded_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(1).
