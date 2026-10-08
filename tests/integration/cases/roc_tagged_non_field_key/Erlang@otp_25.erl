-module(fixture_roc_tagged_non_field_key_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "not-a-field" => 1
    },
    My_data.
