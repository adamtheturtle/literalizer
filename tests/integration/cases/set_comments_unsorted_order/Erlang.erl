-module(check).
-export([x/0]).
x() ->
    sets:from_list([
    % before apple
    "apple",
    "banana"  % banana inline
    % trailing
]).
