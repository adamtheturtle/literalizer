-module(fixture_call_comments_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    % Test cases
    process("hello"),  % single word
    process("hello world"),  % two words
    % trailing comment.
