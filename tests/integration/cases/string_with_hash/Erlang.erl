-module(check).
-export([x/0]).
x() ->
    My_data = [
        "issue #{42}",
        "color #red"
    ],
    My_data.
