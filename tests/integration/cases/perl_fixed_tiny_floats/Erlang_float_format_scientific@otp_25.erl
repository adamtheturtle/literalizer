-module(fixture_perl_fixed_tiny_floats_erlang_float_format_scientific).
-export([x/0]).
x() ->
    My_data = [
        5.0e-324,
        -5.0e-324,
        2.2250738585072014e-308
    ],
    My_data.
