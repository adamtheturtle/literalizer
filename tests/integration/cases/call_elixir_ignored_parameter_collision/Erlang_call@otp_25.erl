-module(fixture_call_elixir_ignored_parameter_collision_erlang_call).
-export([x/0]).
f(_, _) -> ok.
x() ->
    f(1, 2).
