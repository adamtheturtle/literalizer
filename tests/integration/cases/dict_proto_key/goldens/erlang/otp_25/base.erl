-module(fixture_dict_proto_key_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "__proto__" => #{"x" => 1},
        "n" => #{"__proto__" => 3},
        "y" => 2
    },
    My_data.
