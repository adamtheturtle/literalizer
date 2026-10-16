-module(fixture_kotlin_map_of_int_arrays_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "a" => {{1, 2}},
        "b" => {{3}}
    },
    My_data.
