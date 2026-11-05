-module(fixture_roundtrip_verifier_excluded_value_changed_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "keep" => true,
        "skip" => false
    },
    My_data.
