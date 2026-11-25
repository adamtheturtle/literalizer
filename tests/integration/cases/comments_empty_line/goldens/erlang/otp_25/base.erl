-module(fixture_comments_empty_line_erlang).
-export([x/0]).
x() ->
    My_data = [
        "a",
        %
        "b"
    ],
    My_data.
