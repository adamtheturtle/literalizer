-module(fixture_v_empty_map_nested_value_erlang).
-export([x/0]).
x() ->
    My_data = [
        [#{"mapping" => #{}}, #{}],
        [#{}, #{"mapping" => #{}}]
    ],
    My_data.
