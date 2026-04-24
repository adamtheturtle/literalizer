-module(check).
-export([x/0]).
process(_) -> undefined.
x() ->
    process("hello"),
    process(42),
    process(true).
