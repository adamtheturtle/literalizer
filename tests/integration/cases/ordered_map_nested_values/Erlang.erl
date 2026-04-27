-module(fixture_ordered_map_nested_values_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"name", "Alice"},
        {"scores", #{"1" => "first", "2" => "second"}}
    ],
    My_data.
