-module(fixture_yaml_tagged_scalars_erlang_yaml_tagged_scalars).
-export([x/0]).
x() ->
    My_data = #{
        "explicit_string" => "5",
        "six" => "explicitly tagged key"
    },
    My_data.
