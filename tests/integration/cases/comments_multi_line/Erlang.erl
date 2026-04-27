-module(fixture_comments_multi_line_erlang).
-export([x/0]).
x() ->
    My_data = [
        % line 1
        % line 2
        "a"
    ],
    My_data.
