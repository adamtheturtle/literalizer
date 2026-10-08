-module(fixture_yaml_pairs_tag_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"first" => 1},
        #{"repeated" => "a"},
        #{"repeated" => "b"}
    ],
    My_data.
