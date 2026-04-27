-module(fixture_date_set_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        "2024-01-15",
        "2024-06-01"
    ]),
    My_data.
