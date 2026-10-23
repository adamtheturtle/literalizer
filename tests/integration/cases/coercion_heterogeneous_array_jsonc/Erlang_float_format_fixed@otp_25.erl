-module(fixture_coercion_heterogeneous_array_jsonc_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = [
        1,
        2.500000,
        3
    ],
    My_data.
