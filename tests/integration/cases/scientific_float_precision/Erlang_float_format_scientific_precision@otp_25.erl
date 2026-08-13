-module(fixture_scientific_float_precision_erlang_float_format_scientific_precision).
-export([x/0]).
x() ->
    My_data = #{
        "value" => 1.2345678901234567
    },
    My_data.
