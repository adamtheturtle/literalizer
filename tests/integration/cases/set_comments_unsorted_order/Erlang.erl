-module(check).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        % before apple
        "apple",
        "banana"  % banana inline
        % trailing
    ]),
    My_data.
