-module(fixture_times_heterogeneous_with_dates_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "vals" => ["2024-01-15", "09:30:00"]
    },
    My_data.
