-module(fixture_nested_empty_inner_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [],
        []
    ],
    My_data.
