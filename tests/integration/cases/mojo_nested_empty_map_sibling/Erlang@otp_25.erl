-module(fixture_mojo_nested_empty_map_sibling_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"mapping" => #{}},
        #{}
    ],
    My_data.
