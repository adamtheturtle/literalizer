-module(fixture_call_parameter_case_sensitive_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(42).
