-module(fixture_date_set_erlang_date_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        {2024, 1, 15},
        {2024, 6, 1}
    ]),
    My_data.
