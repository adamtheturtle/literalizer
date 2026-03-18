-module(check).
-export([x/0]).
x() ->
    My_data = "hello \"world\" -- not a comment",
    My_data.
