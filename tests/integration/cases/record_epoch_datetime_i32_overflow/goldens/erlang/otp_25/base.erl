-module(fixture_record_epoch_datetime_i32_overflow_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "within_i32" => "2024-01-15T12:00:00",
        "beyond_i32" => "2099-06-15T08:30:00"
    },
    My_data.
