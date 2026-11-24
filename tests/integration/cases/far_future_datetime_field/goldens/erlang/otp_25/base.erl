-module(fixture_far_future_datetime_field_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "ts" => "3000-12-31T23:59:59.999999+00:00"
    },
    My_data.
