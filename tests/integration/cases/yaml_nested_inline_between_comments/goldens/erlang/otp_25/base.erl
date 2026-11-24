-module(fixture_yaml_nested_inline_between_comments_erlang).
-export([x/0]).
x() ->
    My_data = [
        [2, "hello"],  % trailing note
        % next element
        [3, "world"]
    ],
    My_data.
