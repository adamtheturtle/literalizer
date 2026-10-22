-module(fixture_map_mixed_int_widths_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 16#1,
        "b" => 16#10000000000
    },
    My_data.
