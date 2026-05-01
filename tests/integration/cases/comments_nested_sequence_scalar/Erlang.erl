-module(fixture_comments_nested_sequence_scalar_erlang).
-export([x/0]).
x() ->
    My_data = [
        ["ADD", "alice", "hello"],
        ["DEL", "bob", "5"]  % removes "world"
    ],
    My_data.
