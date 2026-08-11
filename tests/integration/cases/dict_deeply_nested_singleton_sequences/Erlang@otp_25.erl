-module(fixture_dict_deeply_nested_singleton_sequences_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "deep" => [[[[1]]]]
    },
    My_data.
