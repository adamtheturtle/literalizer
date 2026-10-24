-module(fixture_call_reserved_target_casefold_erlang_call).
-export([x/0]).
'BEGIN'(_) -> ok.
x() ->
    'BEGIN'(42).
