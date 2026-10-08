-module(fixture_rust_empty_map_sibling_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"a" => 1},
        #{}
    ],
    My_data.
