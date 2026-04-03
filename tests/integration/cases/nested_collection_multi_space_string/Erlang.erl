-module(check).
-export([x/0]).
x() ->
    My_data = [
        #{"key" => "hello   world", "value" => 1}
    ],
    My_data.
