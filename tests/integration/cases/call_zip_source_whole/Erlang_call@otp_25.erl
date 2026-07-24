-module(fixture_call_zip_source_whole_erlang_call).
-export([x/0]).
process(_) -> undefined.
emit(_, _) -> ok.
x() ->
    emit(process(42), "one").
