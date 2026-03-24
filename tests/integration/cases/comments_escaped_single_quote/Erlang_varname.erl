-module(check).
-export([my_data/0]).
my_data() ->
    My_data = #{
    "key" => "it's here"  % a comment
},
    My_data.
