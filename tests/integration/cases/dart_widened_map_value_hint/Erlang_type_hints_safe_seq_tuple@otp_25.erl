-module(fixture_dart_widened_map_value_hint_erlang_type_hints_safe_seq_tuple).
-export([x/0]).
x() ->
    My_data = {
        #{"a" => 1},
        1,
        "x",
        true,
        2.5,
        undefined
    },
    My_data.
