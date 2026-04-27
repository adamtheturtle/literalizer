-module(fixture_datetime_list_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = [
        {{2024, 1, 15}, {12, 30, 0}},
        {{2024, 6, 1}, {8, 0, 0}}
    ],
    My_data.
