-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    1000000,
    -1234,
    255,
    -10
],
    My_data.
