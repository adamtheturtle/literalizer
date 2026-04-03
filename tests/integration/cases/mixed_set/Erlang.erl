-module(check).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        true,
        42,
        "apple"
    ]),
    My_data.
