-module(fixture_call_nested_list_whole_argument_erlang_collection_layout_multiline_call_layout_forced_multiline).
-export([x/0]).
f(_) -> ok.
x() ->
    f([
        [
            1,
            2
        ],
        [
            3
        ]
    ]).
