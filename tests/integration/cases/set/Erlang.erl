-module(check).
-export([x/0]).
x() ->
    sets:from_list([
    "apple",
    "banana",
    "cherry"
]).
