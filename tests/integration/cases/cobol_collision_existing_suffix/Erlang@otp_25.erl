-module(fixture_cobol_collision_existing_suffix_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a-b" => 1,
        "a-b-2" => 2,
        "a b" => 3
    },
    My_data.
