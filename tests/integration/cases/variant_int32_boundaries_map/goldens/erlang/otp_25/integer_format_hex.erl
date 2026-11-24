-module(fixture_variant_int32_boundaries_map_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "below" => -16#80000001,
        "minimum" => -16#80000000,
        "above" => -16#7FFFFFFF,
        "nested" => [16#0]
    },
    My_data.
