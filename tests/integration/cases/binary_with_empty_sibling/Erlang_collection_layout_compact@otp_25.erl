-module(fixture_binary_with_empty_sibling_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        <<72, 101, 108, 108, 111>>,
        []
    ],
    My_data.
