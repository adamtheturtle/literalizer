-module(fixture_literalize_ref_swift_empty_numeric_lists_erlang_ref).
-export([x/0]).
x() ->
    Empty_values = [],
    Integer_values = [
        1
    ],
    Float_values = [
        1.5
    ],
    My_data = [
        Empty_values,
        Integer_values,
        Float_values
    ],
    My_data.
