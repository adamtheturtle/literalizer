-module(fixture_scalar_null_with_comment_erlang).
-export([x/0]).
x() ->
    % note
    My_data = undefined,
    My_data.
