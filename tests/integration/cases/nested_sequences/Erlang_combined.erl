-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    [[1, 2], [3, 4]],
    [[5]]
],
    My_data.
