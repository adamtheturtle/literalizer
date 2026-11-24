-module(fixture_map_of_int_arrays_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [[1, 2]],
        "b" => [[3]]
    },
    My_data.
