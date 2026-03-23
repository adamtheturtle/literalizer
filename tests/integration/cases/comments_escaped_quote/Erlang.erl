-module(check).
-export([x/0]).
x() ->
    #{
    "key" => "value \" # not a comment"  % real
}.
