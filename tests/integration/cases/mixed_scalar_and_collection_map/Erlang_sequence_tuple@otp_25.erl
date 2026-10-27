-module(fixture_mixed_scalar_and_collection_map_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,
        "b" => "x",
        "e" => {1, 2},
        "f" => #{"g" => "h"}
    },
    My_data.
