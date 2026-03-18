-module(check).
-export([x/0]).
x() ->
    "hello \"world\" -- not a comment".
