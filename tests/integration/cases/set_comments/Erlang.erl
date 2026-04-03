-module(check).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        "apple",  % inline comment
        % before banana
        "banana"
        % trailing
    ]),
    My_data.
