-module(fixture_call_wrapper_outer_erlang_call).
-export([x/0]).
process(_) -> undefined.
emit(_) -> ok.
x() ->
    emit(process(42)).
