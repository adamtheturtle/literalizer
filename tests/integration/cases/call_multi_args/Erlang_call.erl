-module(check).
-export([x/0]).
process(_, _) -> ok.
x() ->
    process(1, 42),
    process(2, 100).
