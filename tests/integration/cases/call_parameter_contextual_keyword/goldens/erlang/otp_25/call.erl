-module(fixture_call_parameter_contextual_keyword_erlang_call).
-export([x/0]).
f(_) -> ok.
x() ->
    f(1).
