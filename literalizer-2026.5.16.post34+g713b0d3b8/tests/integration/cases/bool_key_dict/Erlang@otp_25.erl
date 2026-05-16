-module(fixture_bool_key_dict_erlang).
-export([x/0]).
x() ->
    My_data = #{
        true => "yes",
        false => "no"
    },
    My_data.
