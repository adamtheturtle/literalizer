-module(fixture_coercion_homogeneous_array_yaml_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        2,
        3
    ],
    My_data.
