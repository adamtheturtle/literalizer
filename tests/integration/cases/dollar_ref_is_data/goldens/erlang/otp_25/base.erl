-module(fixture_dollar_ref_is_data_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "value" => #{"$ref" => "foo"}
    },
    My_data.
