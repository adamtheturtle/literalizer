-module(check).
-export([x/0]).
x() ->
    My_data = {
        1,
        "hello",
        true,
        undefined
    },
    My_data.
