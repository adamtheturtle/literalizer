-module(fixture_call_parameter_leading_underscore_erlang_call).
-export([x/0]).
f(_) -> ok.
x() ->
    f(1).
