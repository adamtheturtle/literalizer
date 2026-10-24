-module(fixture_positional_empty_map_rows_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "first" => [[1, "value"], []],
        "second" => [[], [2, "other"]]
    },
    My_data.
