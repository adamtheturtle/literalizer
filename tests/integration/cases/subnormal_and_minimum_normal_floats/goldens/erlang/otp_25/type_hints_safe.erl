-module(fixture_subnormal_and_minimum_normal_floats_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        5.0e-324,
        -5.0e-324,
        2.2250738585072014e-308
    ],
    My_data.
