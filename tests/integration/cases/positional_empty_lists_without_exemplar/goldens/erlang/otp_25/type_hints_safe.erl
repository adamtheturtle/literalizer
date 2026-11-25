-module(fixture_positional_empty_lists_without_exemplar_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [[]],
        [[]]
    ],
    My_data.
