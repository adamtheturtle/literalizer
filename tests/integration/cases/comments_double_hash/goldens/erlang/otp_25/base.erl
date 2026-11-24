-module(fixture_comments_double_hash_erlang).
-export([x/0]).
x() ->
    My_data = [
        % # section
        "a"
    ],
    My_data.
