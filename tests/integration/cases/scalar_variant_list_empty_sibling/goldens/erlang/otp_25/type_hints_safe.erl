-module(fixture_scalar_variant_list_empty_sibling_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [1, "value"],
        []
    ],
    My_data.
