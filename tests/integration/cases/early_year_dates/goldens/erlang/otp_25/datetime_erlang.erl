-module(fixture_early_year_dates_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "date" => "0099-05-27",
        "naive" => {{1, 1, 1}, {12, 30, 0}},
        "recent" => {{2024, 5, 27}, {10, 0, 0}}
    },
    My_data.
