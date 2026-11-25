-module(fixture_map_beyond_i64_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 16#7FFFFFFFFFFFFFFF,
        "b" => 16#8000000000000000
    },
    My_data.
