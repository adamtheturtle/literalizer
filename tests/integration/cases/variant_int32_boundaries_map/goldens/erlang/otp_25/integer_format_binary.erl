-module(fixture_variant_int32_boundaries_map_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = #{
        "below" => -2#10000000000000000000000000000001,
        "minimum" => -2#10000000000000000000000000000000,
        "above" => -2#1111111111111111111111111111111,
        "nested" => [2#0]
    },
    My_data.
