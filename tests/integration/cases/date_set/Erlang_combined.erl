-module(check).
-export([my_data/0]).
my_data() ->
    My_data = sets:from_list([
    "2024-01-15",
    "2024-06-01"
]),
    My_data.
