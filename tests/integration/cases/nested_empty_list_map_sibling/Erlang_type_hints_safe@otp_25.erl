-module(fixture_nested_empty_list_map_sibling_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        #{"values" => []},
        #{}
    ],
    My_data.
