-module(fixture_mojo_nested_empty_list_map_sibling_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"values" => []},
        #{}
    ],
    My_data.
