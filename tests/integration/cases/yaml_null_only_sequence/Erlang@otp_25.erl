-module(fixture_yaml_null_only_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        undefined
    ],
    My_data.
