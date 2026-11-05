-module(fixture_roundtrip_verifier_identical_scalar_types_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "value" => [true, false, 0, 1]
    },
    My_data.
