-module(fixture_nested_collection_multi_space_string_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        #{"key" => "hello   world", "value" => 1}
    ],
    My_data.
