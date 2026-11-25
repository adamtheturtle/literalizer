-module(fixture_call_unknown_ref_per_element_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Unknown_value = [],
    process(Unknown_value).
