-module(check).
-export([my_data/0]).
my_data() ->
    My_data = #{
    "name" => "Alice",
    "score" => undefined,
    "age" => 30
},
    My_data.
