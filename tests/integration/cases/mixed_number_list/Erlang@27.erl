-module(fixture_mixed_number_list_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        2.5,
        3
    ],
    My_data.
