-module(fixture_call_shared_wrapper_target_collision_erlang_call).
-export([x/0]).
check(_) -> ok.
x() ->
    check(42).
