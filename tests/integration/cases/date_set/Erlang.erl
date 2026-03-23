-module(check).
-export([x/0]).
x() ->
    sets:from_list([
    "2024-01-15",
    "2024-06-01"
]).
