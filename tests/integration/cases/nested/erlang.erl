-module(check).
-export([x/0]).
x() ->
    #{
    "users" => [#{"name" => "Bob", "tags" => ["admin", "user"]}, #{"name" => "Carol", "tags" => ["guest"]}]
}.
