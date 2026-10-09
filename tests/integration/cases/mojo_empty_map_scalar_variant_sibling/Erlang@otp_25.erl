-module(fixture_mojo_empty_map_scalar_variant_sibling_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"count" => 1, "name" => "value"},
        #{}
    ],
    My_data.
