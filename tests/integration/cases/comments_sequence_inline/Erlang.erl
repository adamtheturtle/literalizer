-module(fixture_comments_sequence_inline_erlang).
-export([x/0]).
x() ->
    My_data = [
        "a",  % note a
        "b"  % note b
    ],
    My_data.
