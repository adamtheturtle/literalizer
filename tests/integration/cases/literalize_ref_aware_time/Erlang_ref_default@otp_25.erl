-module(fixture_literalize_ref_aware_time_erlang_ref_default).
-export([x/0]).
x() ->
    Value = "12:30:15+02:00",
    My_data = #{
        "x" => Value
    },
    My_data.
