-module(fixture_scalar_time_microsecond_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "exact_millisecond" => "09:30:15.123000",
        "sub_millisecond" => "09:30:15.123456"
    },
    My_data.
