-module(fixture_map_of_string_arrays_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = #{
        "a" => ["x"],
        "b" => ["y"]
    },
    My_data.
