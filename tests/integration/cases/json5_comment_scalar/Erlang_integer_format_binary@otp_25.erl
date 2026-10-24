-module(fixture_json5_comment_scalar_erlang_integer_format_binary).
-export([x/0]).
x() ->
    % scalar heading
    % second heading line
    % scalar inline
    % inline continuation
    % scalar trailing
    My_data = 2#101010,
    My_data.
