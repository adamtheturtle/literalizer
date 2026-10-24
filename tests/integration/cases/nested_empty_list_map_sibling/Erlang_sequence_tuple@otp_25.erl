-module(fixture_nested_empty_list_map_sibling_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        #{"values" => {}},
        #{}
    },
    My_data.
