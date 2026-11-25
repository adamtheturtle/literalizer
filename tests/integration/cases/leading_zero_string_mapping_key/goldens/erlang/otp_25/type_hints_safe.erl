-module(fixture_leading_zero_string_mapping_key_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "08" => "value"
    },
    My_data.
