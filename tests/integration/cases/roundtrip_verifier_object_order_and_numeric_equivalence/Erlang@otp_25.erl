-module(fixture_roundtrip_verifier_object_order_and_numeric_equivalence_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "b" => undefined,
        "a" => #{"y" => [1.0], "x" => false}
    },
    My_data.
