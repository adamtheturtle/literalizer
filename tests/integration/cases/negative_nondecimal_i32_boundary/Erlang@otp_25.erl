-module(fixture_negative_nondecimal_i32_boundary_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "minimum" => -2147483648,
        "below" => -3000000000
    },
    My_data.
