-module(fixture_kotlin_list_of_maps_with_lists_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        #{"a" => {1}},
        #{"a" => {2}}
    },
    My_data.
