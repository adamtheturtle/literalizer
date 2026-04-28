-module(fixture_call_dotted_transform_stub_erlang_call).
-export([x/0]).
process(_) -> undefined.
'log.emit'(_) -> ok.
x() ->
    log.emit(process("hello")),
    log.emit(process(42)),
    log.emit(process(true)).
