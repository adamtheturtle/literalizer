-module(fixture_literalize_ref_empty_list_widening_erlang_ref).
-export([x/0]).
x() ->
    Empty_values = [],
    Integer_values = [
        1
    ],
    My_data = [
        Empty_values,
        Integer_values
    ],
    My_data.
