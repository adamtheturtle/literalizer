-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "key\nwith\nnewlines" => "value1",
        "key\twith\ttabs" => "value2",
        "" => "value3"
    },
    My_data.
