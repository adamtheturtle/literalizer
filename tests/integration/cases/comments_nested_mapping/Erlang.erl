-module(check).
-export([x/0]).
x() ->
    #{
    "a" => #{"x" => 1},
    "b" => 2
}.
