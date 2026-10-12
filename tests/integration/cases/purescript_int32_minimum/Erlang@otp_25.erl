-module(fixture_purescript_int32_minimum_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "minimum" => -2147483648,
        "neighbor" => -2147483647,
        "maximum" => 2147483647,
        "nested" => [-2147483648]
    },
    My_data.
