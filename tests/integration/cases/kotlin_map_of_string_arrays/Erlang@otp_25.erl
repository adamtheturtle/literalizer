-module(fixture_kotlin_map_of_string_arrays_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => ["x"],
        "b" => ["y"]
    },
    My_data.
