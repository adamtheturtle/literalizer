-module(fixture_deep_cousin_empty_map_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"outer" => #{"inner" => #{"x" => 1}}},
        #{"outer" => #{"inner" => #{}}}
    ],
    My_data.
