-module(fixture_nested_deep_empty_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = [
        [
            [],
            []
        ]
    ],
    My_data.
