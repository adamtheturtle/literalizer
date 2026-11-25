-module(fixture_nested_collection_type_hint_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "a" => {#{"b" => 1}}
    },
    My_data.
