-module(fixture_empty_key_is_data_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        #{"" => "external_value"}
    ],
    My_data.
