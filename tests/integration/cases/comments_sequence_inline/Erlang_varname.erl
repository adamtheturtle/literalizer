-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    "a",  % note a
    "b"  % note b
],
    My_data.
