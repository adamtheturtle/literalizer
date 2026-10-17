-module(fixture_yaml_rebound_anchor_nested_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [1, [2], 2]
    },
    My_data.
