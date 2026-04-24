-module(check).
-export([x/0]).
process(_) -> ok.
x() ->
    My_var = [
        1,
        2,
        3
    ],
    process(My_var).
