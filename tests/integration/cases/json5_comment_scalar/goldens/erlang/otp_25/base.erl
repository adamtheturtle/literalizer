-module(fixture_json5_comment_scalar_erlang).
-export([x/0]).
x() ->
    % scalar heading
    % second heading line
    % scalar inline
    % inline continuation
    % scalar trailing
    My_data = 42,
    My_data.
