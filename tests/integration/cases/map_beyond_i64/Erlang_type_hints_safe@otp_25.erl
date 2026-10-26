-module(fixture_map_beyond_i64_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 9223372036854775807,
        "b" => 9223372036854775808
    },
    My_data.
