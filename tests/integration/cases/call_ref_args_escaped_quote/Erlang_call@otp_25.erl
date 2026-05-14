-module(fixture_call_ref_args_escaped_quote_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    My_str = "a\"b",
    process(My_str).
