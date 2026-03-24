-module(check).
-export([my_data/0]).
my_data() ->
    sets:from_list([
    "apple",  % inline comment
    % before banana
    "banana"
    % trailing
]).
