-module(fixture_comments_sequence_before_erlang).
-export([x/0]).
x() ->
    My_data = [
        % first
        "a",
        % second
        "b"
    ],
    My_data.
