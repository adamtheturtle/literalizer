-module(fixture_dict_with_nested_list_of_dicts_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [[#{"b" => 1}]]
    },
    My_data.
