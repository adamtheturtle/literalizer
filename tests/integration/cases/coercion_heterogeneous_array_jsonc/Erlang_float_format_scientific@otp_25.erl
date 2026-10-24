-module(fixture_coercion_heterogeneous_array_jsonc_erlang_float_format_scientific).
-export([x/0]).
x() ->
    My_data = [
        1,
        2.5,
        3
    ],
    My_data.
