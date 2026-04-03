-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "users" => [#{"name" => "Bob", "tags" => ["admin", "user"]}, #{"name" => "Carol", "tags" => ["guest"]}]
    },
    My_data.
