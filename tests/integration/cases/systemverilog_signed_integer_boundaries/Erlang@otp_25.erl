-module(fixture_systemverilog_signed_integer_boundaries_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "i32_below" => -2147483649,
        "i32_minimum" => -2147483648,
        "i32_above" => -2147483647,
        "i32_maximum" => 2147483647,
        "i32_over" => 2147483648,
        "i64_minimum" => -9223372036854775808,
        "i64_maximum" => 9223372036854775807
    },
    My_data.
