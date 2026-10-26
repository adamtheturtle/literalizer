-module(fixture_mixed_nested_collection_types_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "lists" => [[1], ["x"], []],
        "maps" => [#{"x" => 1}, #{"x" => "s"}],
        "empties" => #{"a" => [1], "b" => []}
    },
    My_data.
