-module(fixture_nested_i32_and_i64_values_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "values" => [1, 2147483648]
    },
    My_data.
