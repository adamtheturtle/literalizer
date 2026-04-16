-module(check).
-export([x/0]).
x() ->
    My_data = [
        [{"a", 1}],
        "hello"
    ],
    My_data.
