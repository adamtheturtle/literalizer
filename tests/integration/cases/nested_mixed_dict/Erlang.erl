-module(check).
-export([x/0]).
x() ->
    My_data = #{
        "outer" => #{"a" => 1, "b" => "x", "c" => undefined}
    },
    My_data.
