-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    [true, false],
    [true, true]
],
    My_data.
