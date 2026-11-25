-module(fixture_json5_comment_nested_empty_lists_erlang).
-export([x/0]).
x() ->
    My_data = [
        % outer heading
        % first empty
        [],
        % second empty
        []
    ],
    My_data.
