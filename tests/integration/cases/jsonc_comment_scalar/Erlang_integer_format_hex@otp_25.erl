-module(fixture_jsonc_comment_scalar_erlang_integer_format_hex).
-export([x/0]).
x() ->
    % scalar heading
    % second heading line
    % scalar inline
    % inline continuation
    % scalar trailing
    My_data = 16#2A,
    My_data.
