-module(check).
-export([x/0]).
process(_, _) -> ok.
x() ->
    process(1, 2),
    process(3, 4).
