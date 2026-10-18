-module(fixture_ordered_map_proto_key_erlang).
-export([x/0]).
x() ->
    My_data = [
        {"__proto__", #{"x" => 1}},
        {"ordinary", 2}
    ],
    My_data.
