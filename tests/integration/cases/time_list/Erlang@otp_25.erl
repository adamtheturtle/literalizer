-module(fixture_time_list_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "times" => ["09:30:00", "17:45:00", "23:59:59"]
    },
    My_data.
