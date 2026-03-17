-module(check).
-export([x/0]).
x() ->
    My_data = sets:from_list([
    "apple",
    "banana",
    "cherry"
]),
    My_data.
