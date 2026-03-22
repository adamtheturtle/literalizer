-module(check).
-export([x/0]).
x() ->
    [
    #{"key" => "hello   world", "value" => 1}
].
