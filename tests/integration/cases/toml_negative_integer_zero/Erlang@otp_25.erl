-module(fixture_toml_negative_integer_zero_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "value" => -0.0
    },
    My_data.
