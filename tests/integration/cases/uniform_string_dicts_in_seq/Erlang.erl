-module(fixture_uniform_string_dicts_in_seq_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"first" => "Alice", "last" => "Smith"},
        #{"first" => "Bob", "last" => "Jones"}
    ],
    My_data.
