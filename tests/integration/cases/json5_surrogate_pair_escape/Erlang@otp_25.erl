-module(fixture_json5_surrogate_pair_escape_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "astral" => "😀",
        "mixed" => "a😀b",
        "count" => 2,
        "list" => ["😀", 1],
        "nested" => #{"inner" => "😀"}
    },
    My_data.
