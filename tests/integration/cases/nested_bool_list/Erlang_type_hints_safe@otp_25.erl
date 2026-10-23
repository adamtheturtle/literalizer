-module(fixture_nested_bool_list_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        [true, false],
        [true, true]
    ],
    My_data.
