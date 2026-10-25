-module(fixture_call_unknown_ref_values_nested_list_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Unknown_value = [],
    process([Unknown_value]).
