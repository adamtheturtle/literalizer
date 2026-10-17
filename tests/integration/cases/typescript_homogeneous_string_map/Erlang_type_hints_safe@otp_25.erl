-module(fixture_typescript_homogeneous_string_map_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a" => "x",
        "b" => "y"
    },
    My_data.
