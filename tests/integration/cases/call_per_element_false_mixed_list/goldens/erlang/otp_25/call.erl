-module(fixture_call_per_element_false_mixed_list_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process([1, "x"]).
