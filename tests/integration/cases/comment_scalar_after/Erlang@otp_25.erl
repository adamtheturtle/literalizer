-module(fixture_comment_scalar_after_erlang).
-export([x/0]).
x() ->
    % after
    My_data = 42,
    My_data.
