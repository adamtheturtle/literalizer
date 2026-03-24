-module(check).
-export([my_data/0]).
my_data() ->
    #{
    "a" => #{"x" => 1},
    "b" => 2
}.
