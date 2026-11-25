-module(fixture_call_object_proto_parameter_erlang_call).
-export([x/0]).
capture(_) -> ok.
x() ->
    capture(1).
