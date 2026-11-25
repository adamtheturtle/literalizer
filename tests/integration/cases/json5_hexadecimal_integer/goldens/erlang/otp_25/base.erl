-module(fixture_json5_hexadecimal_integer_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "lower" => 3735928559,
        "upper" => 31,
        "negative" => -16,
        "zero" => 0
    },
    My_data.
