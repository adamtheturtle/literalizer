-module(fixture_sequence_of_dicts_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        #{"name" => "Alice", "age" => 30},
        #{"name" => "Bob", "age" => 25}
    ],
    My_data.
