-module(fixture_nested_mixed_dict_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "outer" => #{"a" => 1, "b" => "x", "c" => undefined}
    },
    My_data.
