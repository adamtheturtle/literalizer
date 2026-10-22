-module(fixture_nested_sequence_declaration_modifiers_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [],
        [1],
        [1, 2],
        [1, "x", true, undefined],
        [1, 2, 3, 4, 5, 6, 7, 8]
    ],
    My_data.
