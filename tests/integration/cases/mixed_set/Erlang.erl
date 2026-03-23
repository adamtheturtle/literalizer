-module(check).
-export([x/0]).
x() ->
    sets:from_list([
    true,
    42,
    "apple"
]).
