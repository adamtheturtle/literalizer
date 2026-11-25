-module(fixture_time_dict_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "morning" => "09:30:00",
        "afternoon" => "14:15:00",
        "evening" => "23:59:59"
    },
    My_data.
