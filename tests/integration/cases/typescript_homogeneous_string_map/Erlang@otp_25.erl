-module(fixture_typescript_homogeneous_string_map_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => "x",
        "b" => "y"
    },
    My_data.
