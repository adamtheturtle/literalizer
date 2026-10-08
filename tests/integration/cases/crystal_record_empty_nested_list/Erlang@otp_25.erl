-module(fixture_crystal_record_empty_nested_list_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [[1, 2], [3]],
        "b" => [[], [1]]
    },
    My_data.
