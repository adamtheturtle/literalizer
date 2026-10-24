-module(fixture_nested_sibling_map_matching_values_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "first" => #{"items" => [1, #{"value" => 2}]},
        "second" => #{"items" => [1, #{"value" => 3}]}
    },
    My_data.
