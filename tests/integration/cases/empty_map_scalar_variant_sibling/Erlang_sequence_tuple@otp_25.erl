-module(fixture_empty_map_scalar_variant_sibling_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        #{"count" => 1, "name" => "value"},
        #{}
    },
    My_data.
