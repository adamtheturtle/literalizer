-module(fixture_deep_alternating_singleton_containers_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [#{"a" => [#{"a" => [#{"a" => [#{"a" => [#{"a" => [#{"a" => [#{"a" => [1]}]}]}]}]}]}]}]
    },
    My_data.
