-module(fixture_scientific_float_precision_erlang_float_format_scientific_precision).
-export([x/0]).
x() ->
    My_data = #{
        "pi" => 3.141592653589793
    },
    My_data.
