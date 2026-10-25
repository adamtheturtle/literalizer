-module(fixture_sibling_mixed_scalar_sequences_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "left" => [1, "one"],
        "right" => [2, "two"]
    },
    My_data.
