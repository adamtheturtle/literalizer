-module(fixture_nested_maps_with_opposed_value_types_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"input" => #{"name" => "alice", "city" => "paris"}, "expected" => #{"count" => 1, "total" => 2}},
        #{"input" => #{"name" => 10, "city" => 20}, "expected" => #{"count" => "done", "total" => "pending"}}
    ],
    My_data.
