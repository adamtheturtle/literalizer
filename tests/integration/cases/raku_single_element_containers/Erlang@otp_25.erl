-module(fixture_raku_single_element_containers_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "single_map" => [#{}],
        "single_list" => [[1]],
        "single_deep" => [[[2]]]
    },
    My_data.
