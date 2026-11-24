-module(fixture_datetime_epoch_wide_carrier_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "within_i32" => "2024-01-15T12:00:00",
        "beyond_i32" => "2099-06-15T08:30:00"
    },
    My_data.
