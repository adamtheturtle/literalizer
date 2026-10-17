-module(fixture_nested_array_maps_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "groups" => {{#{"id" => 1}}, {#{"id" => 2}}}
    },
    My_data.
