-module(fixture_comment_collection_closing_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        1
        % closing
    },
    My_data.
