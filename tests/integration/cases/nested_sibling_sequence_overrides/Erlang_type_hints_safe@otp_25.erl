-module(fixture_nested_sibling_sequence_overrides_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [[1], [2]],
        "b" => [["x"], ["y"]]
    },
    My_data.
