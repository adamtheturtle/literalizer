-module(fixture_yaml_anchor_marks_in_comment_erlang).
-export([x/0]).
x() ->
    % An anchor and an alias marker, written only inside this comment: &a *a
    My_data = undefined,
    My_data.
