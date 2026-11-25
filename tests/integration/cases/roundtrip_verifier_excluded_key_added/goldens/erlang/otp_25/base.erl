-module(fixture_roundtrip_verifier_excluded_key_added_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "keep" => true,
        "skip" => 0
    },
    My_data.
