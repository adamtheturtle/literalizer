-module(fixture_comment_collection_closing_erlang).
-export([x/0]).
x() ->
    My_data = [
        1
        % closing
    ],
    My_data.
