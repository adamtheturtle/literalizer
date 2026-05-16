-module(fixture_call_line_comments_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process("Dune"),  % first edition
    process("Solaris"),
    process("Neuromancer"),  % cyberpunk.
