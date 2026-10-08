-module(fixture_csharp_array_map_element_type_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "d" => {#{"a" => {#{"b" => {1, {2.5, {"x", {true}}}}}}}}
    },
    My_data.
