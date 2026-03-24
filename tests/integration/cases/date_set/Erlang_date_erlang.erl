-module(check).
-export([my_data/0]).
my_data() ->
    sets:from_list([
    {2024, 1, 15},
    {2024, 6, 1}
]).
