-module(fixture_v_four_dimensional_empty_lists_erlang).
-export([x/0]).
x() ->
    My_data = [
        [
            [
                []
            ]
        ],
        [
            [
                []
            ]
        ]
    ],
    My_data.
