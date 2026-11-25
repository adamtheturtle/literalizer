-module(fixture_dates_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "date" => "2024-01-15",
        "datetime" => "2024-01-15T12:30:00+00:00"
    },
    My_data.
