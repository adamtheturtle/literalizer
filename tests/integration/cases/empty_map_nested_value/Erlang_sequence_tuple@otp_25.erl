-module(fixture_empty_map_nested_value_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {#{"mapping" => #{}}, #{}},
        {#{}, #{"mapping" => #{}}}
    },
    My_data.
