-module(check).
-export([x/0]).
process(_) -> ok.
x() ->
    process(1).
