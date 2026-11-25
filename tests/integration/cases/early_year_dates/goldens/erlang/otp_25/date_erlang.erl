-module(fixture_early_year_dates_erlang_date_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "date" => {99, 5, 27},
        "naive" => "0001-01-01T12:30:00",
        "recent" => "2024-05-27T10:00:00"
    },
    My_data.
