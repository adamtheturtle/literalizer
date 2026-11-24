-module(fixture_call_zip_ignored_preamble_erlang_call).
-export([x/0]).
process(_) -> undefined.
x() ->
    process(1),
    process(2).
