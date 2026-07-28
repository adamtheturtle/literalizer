-module(fixture_call_unknown_ref_top_level_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Unknown_value = [
        1
    ],
    process(Unknown_value).
