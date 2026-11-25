-module(fixture_narrowed_empty_list_map_values_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [1],
        "b" => []
    },
    My_data.
