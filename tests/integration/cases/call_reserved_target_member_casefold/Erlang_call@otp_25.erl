-module(fixture_call_reserved_target_member_casefold_erlang_call).
-export([x/0]).
'obj.BEGIN'(_) -> ok.
x() ->
    'obj.BEGIN'(42).
