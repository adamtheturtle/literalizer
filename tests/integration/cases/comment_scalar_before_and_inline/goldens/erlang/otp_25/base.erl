-module(fixture_comment_scalar_before_and_inline_erlang).
-export([x/0]).
x() ->
    % before
    % inline
    My_data = "plain",
    My_data.
