-module(check).
-export([my_data/0]).
my_data() ->
    #{
    "users" => [#{"name" => "Bob", "tags" => ["admin", "user"]}, #{"name" => "Carol", "tags" => ["guest"]}]
}.
