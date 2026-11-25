-module(fixture_int32_minimum_with_nested_list_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = #{
        "minimum" => -2#10000000000000000000000000000000,
        "neighbor" => -2#1111111111111111111111111111111,
        "maximum" => 2#1111111111111111111111111111111,
        "nested" => [-2#10000000000000000000000000000000]
    },
    My_data.
