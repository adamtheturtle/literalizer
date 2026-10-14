-module(fixture_call_rust_epoch_boundary_erlang_datetime_epoch_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    consume(-2147483649),
    consume(2147483648).
