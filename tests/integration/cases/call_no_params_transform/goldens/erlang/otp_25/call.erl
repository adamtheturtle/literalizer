-module(fixture_call_no_params_transform_erlang_call).
-export([x/0]).
process() -> undefined.
emit(_) -> ok.
x() ->
    emit(process()),
    emit(process()).
