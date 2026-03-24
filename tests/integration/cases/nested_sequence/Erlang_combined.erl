-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    true,
    "hi",
    [1, 2],
    undefined
],
    My_data.
