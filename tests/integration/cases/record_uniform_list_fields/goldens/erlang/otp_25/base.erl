-module(fixture_record_uniform_list_fields_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"scores" => [1, 2]},
        #{"scores" => [3, 4]}
    ],
    My_data.
