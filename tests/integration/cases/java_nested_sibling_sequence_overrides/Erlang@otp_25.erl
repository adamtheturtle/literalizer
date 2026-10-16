-module(fixture_java_nested_sibling_sequence_overrides_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [[1], [2]],
        "b" => [["x"], ["y"]]
    },
    My_data.
