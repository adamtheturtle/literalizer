-module(fixture_call_null_and_array_arguments_erlang_collection_layout_multiline_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(undefined),
    process([
        1,
        2
    ]).
