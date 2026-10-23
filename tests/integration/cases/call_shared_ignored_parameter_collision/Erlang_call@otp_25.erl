-module(fixture_call_shared_ignored_parameter_collision_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    process(1, 2).
