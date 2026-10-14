-module(fixture_cpp_variant_int32_boundaries_map_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "below" => -2147483649,
        "minimum" => -2147483648,
        "above" => -2147483647,
        "nested" => [0]
    },
    My_data.
