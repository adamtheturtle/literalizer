-module(fixture_record_empty_nested_list_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [[1, 2], [3]],
        "b" => [[], [1]]
    },
    My_data.
