-module(fixture_roundtrip_verifier_float_array_as_integers_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "value" => [0, 1]
    },
    My_data.
