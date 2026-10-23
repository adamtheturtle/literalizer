-module(fixture_bool_key_dict_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = #{
        true => "yes",
        false => "no"
    },
    My_data.
