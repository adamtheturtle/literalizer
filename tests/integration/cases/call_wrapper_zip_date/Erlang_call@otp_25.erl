-module(fixture_call_wrapper_zip_date_erlang_call).
-export([x/0]).
process(_) -> undefined.
emit(_, _) -> ok.
x() ->
    emit(process(1), "2024-01-15").
