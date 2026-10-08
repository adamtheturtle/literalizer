-module(fixture_go_widened_dict_elements_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [#{}, #{"x" => 1}],
        "b" => [[], [1]]
    },
    My_data.
