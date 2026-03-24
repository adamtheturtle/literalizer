-module(check).
-export([my_data/0]).
my_data() ->
    My_data = #{
    "message" => "no comment here"
},
    My_data.
