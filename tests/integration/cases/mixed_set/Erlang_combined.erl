-module(check).
-export([my_data/0]).
my_data() ->
    My_data = sets:from_list([
    true,
    42,
    "apple"
]),
    My_data.
