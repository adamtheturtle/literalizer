-module(fixture_narrowed_empty_list_mixed_sibling_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [1, "two"],
        []
    ],
    My_data.
