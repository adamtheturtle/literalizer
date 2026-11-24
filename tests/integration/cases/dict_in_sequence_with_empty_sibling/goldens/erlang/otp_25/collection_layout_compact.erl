-module(fixture_dict_in_sequence_with_empty_sibling_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        #{"a" => 1},
        []
    ],
    My_data.
