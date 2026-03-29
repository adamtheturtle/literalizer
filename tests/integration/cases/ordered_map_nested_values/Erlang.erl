-module(check).
-export([x/0]).
x() ->
    My_data = [
    {"name", "Alice"},
    {"scores", #{"1" => "first", "2" => "second"}}
],
    My_data.
