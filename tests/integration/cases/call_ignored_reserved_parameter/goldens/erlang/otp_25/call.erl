-module(fixture_call_ignored_reserved_parameter_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(42).
