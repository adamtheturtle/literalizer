-module(fixture_toml_extreme_exponent_zero_erlang_float_format_fixed).
-export([x/0]).
x() ->
    My_data = #{
        "value" => 0.000000
    },
    My_data.
