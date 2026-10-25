-module(fixture_call_datetime_epoch_boundary_erlang_datetime_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    consume({{1901, 12, 13}, {20, 45, 51}}),
    consume({{2038, 1, 19}, {3, 14, 8}}).
