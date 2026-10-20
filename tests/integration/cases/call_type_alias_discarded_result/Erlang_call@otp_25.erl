-module(fixture_call_type_alias_discarded_result_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(1).
