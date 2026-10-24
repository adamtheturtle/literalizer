-module(fixture_tuple_empty_map_values_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "filled" => [1, "value"],
        "empty" => []
    },
    My_data.
