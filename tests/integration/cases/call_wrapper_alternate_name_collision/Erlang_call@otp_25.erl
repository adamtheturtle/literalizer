-module(fixture_call_wrapper_alternate_name_collision_erlang_call).
-export([x/0]).
check_wrapper(_) -> ok.
x() ->
    check_wrapper(42).
