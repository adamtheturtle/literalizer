-module(fixture_call_zip_opaque_emitted_erlang_datetime_erlang_call).
-export([x/0]).
process(_) -> undefined.
emit(_, _) -> ok.
x() ->
    emit(process(1), {{2024, 1, 15}, {12, 0, 0}}).
