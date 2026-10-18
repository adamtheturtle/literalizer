-module(fixture_kotlin_map_of_wide_int_lists_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "a" => {4294967296, 4294967297}
    },
    My_data.
