-module(check).
-export([my_data/0]).
my_data() ->
    sets:from_list([
    % before apple
    "apple",
    "banana"  % banana inline
    % trailing
]).
