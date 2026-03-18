-module(check).
-export([x/0]).
x() ->
    #{
    "key\nwith\nnewlines" => "value1",
    "key	with	tabs" => "value2"
}.
