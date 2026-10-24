-module(fixture_comment_scalar_after_erlang_integer_format_hex).
-export([x/0]).
x() ->
    % after
    My_data = 16#2A,
    My_data.
