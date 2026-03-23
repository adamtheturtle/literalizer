-module(check).
-export([x/0]).
x() ->
    sets:from_list([
    1,
    2,
    3
]).
