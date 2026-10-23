-module(fixture_comment_scalar_document_markers_erlang_integer_format_binary).
-export([x/0]).
x() ->
    % note
    My_data = 2#101010,
    My_data.
