-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "key" => "\"bang!\""  % real
    },
    My_data.
