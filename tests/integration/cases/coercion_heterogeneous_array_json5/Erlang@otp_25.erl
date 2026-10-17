-module(fixture_coercion_heterogeneous_array_json5_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        2.5,
        3
    ],
    My_data.
