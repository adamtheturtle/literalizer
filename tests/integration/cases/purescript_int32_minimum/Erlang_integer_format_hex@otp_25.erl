-module(fixture_purescript_int32_minimum_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "minimum" => -16#80000000,
        "neighbor" => -16#7FFFFFFF,
        "maximum" => 16#7FFFFFFF,
        "nested" => [-16#80000000]
    },
    My_data.
