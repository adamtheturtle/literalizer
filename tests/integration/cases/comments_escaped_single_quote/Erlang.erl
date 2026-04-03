-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "key" => "it's here"  % a comment
    },
    My_data.
