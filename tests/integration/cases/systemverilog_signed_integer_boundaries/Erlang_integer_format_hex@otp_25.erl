-module(fixture_systemverilog_signed_integer_boundaries_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "i32_below" => -16#80000001,
        "i32_minimum" => -16#80000000,
        "i32_above" => -16#7FFFFFFF,
        "i32_maximum" => 16#7FFFFFFF,
        "i32_over" => 16#80000000,
        "i64_minimum" => -16#8000000000000000,
        "i64_maximum" => 16#7FFFFFFFFFFFFFFF
    },
    My_data.
