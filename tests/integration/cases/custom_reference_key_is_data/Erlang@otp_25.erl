-module(fixture_custom_reference_key_is_data_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "reference" => "whole"
    },
    My_data.
