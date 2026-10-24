-module(fixture_call_reserved_target_head_erlang_call).
-export([x/0]).
'class.member'(_) -> ok.
x() ->
    'class.member'(42).
