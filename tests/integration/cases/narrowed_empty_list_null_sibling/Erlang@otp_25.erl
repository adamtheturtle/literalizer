-module(fixture_narrowed_empty_list_null_sibling_erlang).
-export([x/0]).
x() ->
    My_data = [
        [undefined],
        []
    ],
    My_data.
