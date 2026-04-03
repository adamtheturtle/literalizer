-module(check).
-export([x/0]).
x() ->
    My_data = [
        "prefix ${HOME} suffix",
        "${interpolated}"
    ],
    My_data.
