-module(fixture_coercion_homogeneous_array_toml_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "_" => [1, 2, 3]
    },
    My_data.
