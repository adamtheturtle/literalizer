-module(fixture_set_comments_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        "apple",  % inline comment
        % before banana
        "banana"
        % trailing
    ]),
    My_data.
