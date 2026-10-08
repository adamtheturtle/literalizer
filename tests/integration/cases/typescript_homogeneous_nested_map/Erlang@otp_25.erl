-module(fixture_typescript_homogeneous_nested_map_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "first" => #{"x" => 1, "y" => 2},
        "second" => #{"z" => 3}
    },
    My_data.
