-module(fixture_empty_list_map_values_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [1],
        "b" => []
    },
    My_data.
