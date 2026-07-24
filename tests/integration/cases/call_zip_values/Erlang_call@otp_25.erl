-module(fixture_call_zip_values_erlang_call).
-export([x/0]).
process(_) -> undefined.
emit(_, _) -> ok.
x() ->
    emit(process("hello"), "one"),
    emit(process(42), "zero").
