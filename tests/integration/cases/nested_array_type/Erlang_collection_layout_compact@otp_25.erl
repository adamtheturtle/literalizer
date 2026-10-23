-module(fixture_nested_array_type_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        [[1]]
    ],
    My_data.
