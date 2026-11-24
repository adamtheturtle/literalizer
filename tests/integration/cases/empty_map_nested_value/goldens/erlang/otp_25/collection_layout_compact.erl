-module(fixture_empty_map_nested_value_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = [
        [#{"mapping" => #{}}, #{}],
        [#{}, #{"mapping" => #{}}]
    ],
    My_data.
