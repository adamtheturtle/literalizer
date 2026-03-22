-module(check).
-export([x/0]).
x() ->
    #{
    "date" => {2024, 1, 15},
    "datetime" => {{2024, 1, 15}, {12, 30, 0}}
}.
