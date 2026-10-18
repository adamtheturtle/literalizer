-module(fixture_literalize_ref_time_erlang_ref).
-export([x/0]).
x() ->
    My_time = "01:02:03",
    My_data = #{
        "x" => My_time
    },
    My_data.
