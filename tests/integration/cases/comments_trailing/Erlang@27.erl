-module(fixture_comments_trailing_erlang).
-export([x/0]).
x() ->
    My_data = [
        "a"
        % trailing
    ],
    My_data.
