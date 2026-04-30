-module(fixture_dict_dollar_ref_key_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "$ref" => "my_var"
    },
    My_data.
