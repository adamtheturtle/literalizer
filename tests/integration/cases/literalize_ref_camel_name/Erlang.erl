-module(fixture_literalize_ref_camel_name_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "$ref" => "myVar"
    },
    My_data.
