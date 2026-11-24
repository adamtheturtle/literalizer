-module(fixture_nested_collection_multi_space_string_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"key" => "hello   world", "value" => 1}
    ],
    My_data.
