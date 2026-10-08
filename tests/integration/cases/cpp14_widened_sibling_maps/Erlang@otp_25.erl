-module(fixture_cpp14_widened_sibling_maps_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{"k" => 1},
        "b" => #{"k" => "s"}
    },
    My_data.
