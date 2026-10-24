-module(fixture_sibling_maps_in_sequence_rendered_epoch_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        #{"k" => "2040-01-01T00:00:00+00:00"},
        #{"k" => 1}
    },
    My_data.
