-module(fixture_call_wrap_in_file_escaped_quote_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process("a\"b").
