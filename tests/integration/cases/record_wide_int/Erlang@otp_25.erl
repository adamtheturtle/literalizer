-module(fixture_record_wide_int_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "quantity" => 1000000,
        "big" => 18446744073709551615,
        "ratio" => 2.5,
        "label" => "tag",
        "ok" => true
    },
    My_data.
