-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    #{"key" => "hello   world", "value" => 1}
],
    My_data.
