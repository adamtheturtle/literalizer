-module(fixture_empty_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        [],
        #{}
    ],
    My_data.
