-module(fixture_yaml_rebound_anchor_multiple_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [1, [2, 3], 3]
    },
    My_data.
