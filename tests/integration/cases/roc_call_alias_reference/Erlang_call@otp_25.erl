-module(fixture_roc_call_alias_reference_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Value = 1,
    process(Value).
