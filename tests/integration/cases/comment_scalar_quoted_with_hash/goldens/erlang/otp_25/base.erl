-module(fixture_comment_scalar_quoted_with_hash_erlang).
-export([x/0]).
x() ->
    % note
    My_data = "hello # world",
    My_data.
