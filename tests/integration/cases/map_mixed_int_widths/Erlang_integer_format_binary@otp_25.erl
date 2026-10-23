-module(fixture_map_mixed_int_widths_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 2#1,
        "b" => 2#10000000000000000000000000000000000000000
    },
    My_data.
