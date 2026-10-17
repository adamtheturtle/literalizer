-module(fixture_empty_ref_key_erlang_ref_default).
-export([x/0]).
x() ->
    External_value = #{
        "_" => "_"
    },
    My_data = [
        External_value
    ],
    My_data.
