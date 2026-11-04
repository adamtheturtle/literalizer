-module(fixture_call_whole_list_argument_erlang_collection_layout_multiline_call).
-export([x/0]).
f(_) -> ok.
x() ->
    f([
        1
    ]).
