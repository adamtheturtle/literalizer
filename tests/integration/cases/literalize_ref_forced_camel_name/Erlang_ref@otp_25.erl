-module(fixture_literalize_ref_forced_camel_name_erlang_ref).
-export([x/0]).
x() ->
    UserObj = #{
        "_" => "_"
    },
    My_data = UserObj,
    My_data.
