-module(fixture_call_unknown_ref_nested_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    Known_value = true,
    Unknown_value = true,
    process(Known_value, [Unknown_value]).
