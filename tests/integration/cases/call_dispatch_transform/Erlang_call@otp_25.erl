-module(fixture_call_dispatch_transform_erlang_call).
-export([x/0]).
record_value(_) -> undefined.
flush_buffer(_) -> ok.
emit(_) -> ok.
x() ->
    emit(record_value(42)),
    flush_buffer(3).
