-module(fixture_map_of_string_arrays_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a" => ["x"],
        "b" => ["y"]
    },
    My_data.
