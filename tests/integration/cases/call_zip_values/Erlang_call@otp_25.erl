-module(fixture_call_zip_values_erlang_call).
-export([x/0]).
process(_) -> undefined.
emit(_, _) -> ok.
x() ->
    emit(process("hello"), 1),
    emit(process(42), 0).
