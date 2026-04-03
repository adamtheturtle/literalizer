-module(check).
-export([x/0]).
x() ->
    My_data = [
        #{"first" => "Alice", "last" => "Smith"},
        #{"first" => "Bob", "last" => "Jones"}
    ],
    My_data.
