-module(fixture_literalize_ref_integer_float_sibling_erlang_ref).
-export([x/0]).
x() ->
    Integer_value = 1.0,
    My_data = [
        Integer_value,
        1.5
    ],
    My_data.
