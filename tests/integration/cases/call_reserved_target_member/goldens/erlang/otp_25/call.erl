-module(fixture_call_reserved_target_member_erlang_call).
-export([x/0]).
'obj.class'(_) -> ok.
x() ->
    'obj.class'(42).
