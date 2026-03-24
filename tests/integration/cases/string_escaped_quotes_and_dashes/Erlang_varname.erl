-module(check).
-export([my_data/0]).
my_data() ->
    My_data = "hello \"world\" -- not a comment",
    My_data.
