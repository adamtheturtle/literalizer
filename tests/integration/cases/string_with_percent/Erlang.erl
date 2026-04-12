-module(check).
-export([x/0]).
x() ->
    My_data = [
        "100% done",
        "%(name) is here"
    ],
    My_data.
