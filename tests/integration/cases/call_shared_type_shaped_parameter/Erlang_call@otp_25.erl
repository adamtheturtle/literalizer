-module(fixture_call_shared_type_shaped_parameter_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(1).
