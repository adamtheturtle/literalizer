-module(fixture_call_wrapper_target_name_collision_erlang_call).
-export([x/0]).
check(_) -> ok.
x() ->
    check(42).
