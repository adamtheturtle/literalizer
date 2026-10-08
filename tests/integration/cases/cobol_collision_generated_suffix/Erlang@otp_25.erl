-module(fixture_cobol_collision_generated_suffix_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a-b" => 1,
        "a b" => 2,
        "a-b-2" => 3
    },
    My_data.
