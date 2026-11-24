-module(fixture_negative_nondecimal_i32_boundary_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "minimum" => -16#80000000,
        "below" => -16#B2D05E00
    },
    My_data.
