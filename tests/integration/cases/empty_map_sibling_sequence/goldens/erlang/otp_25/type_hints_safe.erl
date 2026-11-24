-module(fixture_empty_map_sibling_sequence_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        #{"a" => 1},
        #{}
    ],
    My_data.
