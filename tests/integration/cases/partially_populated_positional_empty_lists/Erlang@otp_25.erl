-module(fixture_partially_populated_positional_empty_lists_erlang).
-export([x/0]).
x() ->
    My_data = [
        [
            [],
            []
        ],
        [
            [],
            [
                1
            ]
        ]
    ],
    My_data.
