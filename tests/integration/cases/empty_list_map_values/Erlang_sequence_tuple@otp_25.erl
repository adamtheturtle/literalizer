-module(fixture_empty_list_map_values_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "a" => {1},
        "b" => {}
    },
    My_data.
