-module(check).
-export([x/0]).
process(_) -> ok.
x() ->
    process("hello"),
    process(42),
    process(true).
