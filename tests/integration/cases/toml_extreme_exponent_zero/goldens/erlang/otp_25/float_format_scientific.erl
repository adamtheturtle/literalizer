-module(fixture_toml_extreme_exponent_zero_erlang_float_format_scientific).
-export([x/0]).
x() ->
    My_data = #{
        "value" => 0.0
    },
    My_data.
