-module(fixture_nested_empty_inner_erlang_collection_layout_multiline).
-export([x/0]).
x() ->
    My_data = [
        [],
        []
    ],
    My_data.
