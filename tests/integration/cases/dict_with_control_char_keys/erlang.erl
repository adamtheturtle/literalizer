-module(check).
-export([x/0]).
x() ->
    #{
    "key\nwith\nnewlines" => "value1",
    "key\twith\ttabs" => "value2",
    "" => "value3"
}.
