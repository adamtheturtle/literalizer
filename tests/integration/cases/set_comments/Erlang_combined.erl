-module(check).
-export([my_data/0]).
my_data() ->
    My_data = sets:from_list([
    "apple",  % inline comment
    % before banana
    "banana"
    % trailing
]),
    My_data.
