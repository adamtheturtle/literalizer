-module(fixture_dict_wide_int_key_erlang).
-export([x/0]).
x() ->
    My_data = #{
        99999999999999999999999999 => "tag"
    },
    My_data.
