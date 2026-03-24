-module(check).
-export([my_data/0]).
my_data() ->
    My_data = #{
    "key" => "\"bang!\""  % real
},
    My_data.
