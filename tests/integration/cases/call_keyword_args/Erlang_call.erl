-module(check).
-export([x/0]).
'throttler.check'(_, _) -> undefined.
emit(_) -> ok.
x() ->
    emit('throttler.check'("user_1", 1000.0)),
    emit('throttler.check'("user_2", 2000.5)).
