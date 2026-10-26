-module(fixture_call_zip_opaque_emitted_erlang_datetime_epoch_call).
-export([x/0]).
process(_) -> undefined.
emit(_, _) -> ok.
x() ->
    emit(process(1), 1705320000).
