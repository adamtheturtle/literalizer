-module(fixture_mixed_nested_collection_types_erlang_plain_collection_callbacks).
-export([x/0]).
x() ->
    My_data = #{
        "lists" => [[1], ["x"], []],
        "maps" => [#{"x" => 1}, #{"x" => "s"}],
        "empties" => #{"a" => [1], "b" => []}
    },
    My_data.
