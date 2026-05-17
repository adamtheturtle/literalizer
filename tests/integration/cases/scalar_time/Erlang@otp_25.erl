-module(fixture_scalar_time_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "starts_at" => "09:30:00"
    },
    My_data.
