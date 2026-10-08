-module(fixture_negative_nondecimal_i32_boundary_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = #{
        "minimum" => -2#10000000000000000000000000000000,
        "below" => -2#10110010110100000101111000000000
    },
    My_data.
