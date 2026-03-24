-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    1,
    "hello",
    true
],
    My_data.
