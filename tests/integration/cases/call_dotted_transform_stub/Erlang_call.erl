-module(fixture_call_dotted_transform_stub_erlang_call).
-export([x/0]).
process(_) -> undefined.
'tracer.emit'(_) -> ok.
x() ->
    tracer.emit(process("hello")),
    tracer.emit(process(42)),
    tracer.emit(process(true)).
