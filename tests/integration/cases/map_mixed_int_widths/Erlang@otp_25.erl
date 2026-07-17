-module(fixture_map_mixed_int_widths_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,
        "b" => 1099511627776
    },
    My_data.
