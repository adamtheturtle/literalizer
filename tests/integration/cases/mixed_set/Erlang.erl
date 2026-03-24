-module(check).
-export([my_data/0]).
my_data() ->
    sets:from_list([
    true,
    42,
    "apple"
]).
