-module(fixture_roc_call_alias_bound_erlang_call).
-export([x/0]).
process(_) -> undefined.
x() ->
    My_data = process(1),
    My_data.
