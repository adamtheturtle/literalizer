-module(check).
-export([my_data/0]).
my_data() ->
    My_data = #{
    "key\nwith\nnewlines" => "value1",
    "key\twith\ttabs" => "value2",
    "" => "value3"
},
    My_data.
