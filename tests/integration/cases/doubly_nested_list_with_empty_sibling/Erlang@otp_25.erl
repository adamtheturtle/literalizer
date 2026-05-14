-module(fixture_doubly_nested_list_with_empty_sibling_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[1, 2]],
        [],
        [[3, 4]]
    ],
    My_data.
