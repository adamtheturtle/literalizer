-module(check).
-export([x/0]).
x() ->
    My_data = #{
    "date" => {2024, 1, 15},
    "datetime" => {{2024, 1, 15}, {12, 30, 0}}
},
    My_data.
