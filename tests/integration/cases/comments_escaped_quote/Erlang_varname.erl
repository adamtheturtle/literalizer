-module(check).
-export([my_data/0]).
my_data() ->
    My_data = #{
    "key" => "value \" # not a comment"  % real
},
    My_data.
