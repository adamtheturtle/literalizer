-module(check).
-export([my_data/0]).
my_data() ->
    My_data = #{
    "a" => 1,
    "b" => 2.5,
    "c" => 3
},
    My_data.
