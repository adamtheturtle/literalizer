-module(fixture_call_per_element_false_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(1).
