-module(fixture_roundtrip_verifier_integer_as_float_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "value" => 1.0
    },
    My_data.
