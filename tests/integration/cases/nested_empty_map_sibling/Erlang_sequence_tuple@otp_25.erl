-module(fixture_nested_empty_map_sibling_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        #{"mapping" => #{}},
        #{}
    },
    My_data.
