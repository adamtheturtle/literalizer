-module(fixture_mojo_empty_map_epoch_sibling_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"timestamp" => "2020-01-01T00:00:00+00:00"},
        #{}
    ],
    My_data.
