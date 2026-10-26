-module(fixture_nested_underscore_dict_key_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "outer" => [#{"_" => 1}]
    },
    My_data.
