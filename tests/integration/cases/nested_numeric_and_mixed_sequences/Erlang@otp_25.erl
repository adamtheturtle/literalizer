-module(fixture_nested_numeric_and_mixed_sequences_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "numbers" => [1, 2],
        "nested" => #{"inner" => [3]},
        "mixed" => [4, "five"]
    },
    My_data.
