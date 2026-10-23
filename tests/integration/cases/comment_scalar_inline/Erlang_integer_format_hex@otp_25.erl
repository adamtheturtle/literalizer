-module(fixture_comment_scalar_inline_erlang_integer_format_hex).
-export([x/0]).
x() ->
    % note
    My_data = 16#2A,
    My_data.
