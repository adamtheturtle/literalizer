-module(fixture_literalize_ref_numeric_widening_erlang_ref).
-export([x/0]).
x() ->
    Floating_value = 1.5,
    Integer_value = 2.0,
    My_data = [
        Floating_value,
        Integer_value
    ],
    My_data.
