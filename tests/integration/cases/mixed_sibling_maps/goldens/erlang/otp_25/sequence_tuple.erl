-module(fixture_mixed_sibling_maps_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {#{"a" => 1}, #{"a" => undefined}, 42},
        {#{"a" => 1}, #{"a" => "s"}, 42},
        {#{"a" => 1}, #{"a" => undefined}},
        {#{"a" => 1}, #{"a" => "s"}}
    },
    My_data.
