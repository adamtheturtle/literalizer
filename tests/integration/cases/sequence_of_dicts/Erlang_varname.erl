-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    #{"name" => "Alice", "age" => 30},
    #{"name" => "Bob", "age" => 25}
],
    My_data.
