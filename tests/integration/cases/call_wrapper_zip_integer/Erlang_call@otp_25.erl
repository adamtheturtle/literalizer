-module(fixture_call_wrapper_zip_integer_erlang_call).
-export([x/0]).
process(_) -> undefined.
emit(_, _) -> ok.
x() ->
    emit(process(1), 42).
