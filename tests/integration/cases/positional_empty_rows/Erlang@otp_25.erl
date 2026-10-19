-module(fixture_positional_empty_rows_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[1, "value"], []],
        [[], [2, "other"]]
    ],
    My_data.
