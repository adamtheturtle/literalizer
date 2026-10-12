-module(fixture_call_ref_rust_repeated_owned_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Item = [
        1,
        2
    ],
    process(Item),
    process(Item).
