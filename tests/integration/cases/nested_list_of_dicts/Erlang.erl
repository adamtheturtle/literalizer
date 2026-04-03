-module(check).
-export([x/0]).
x() ->
    My_data = [
        [#{"name" => "Alice"}, #{"name" => "Bob"}],
        [#{"name" => "Charlie"}, #{"name" => "Dave"}]
    ],
    My_data.
