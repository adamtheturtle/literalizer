-module(fixture_call_ref_nested_in_list_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[#{"$ref" => "my_var"}, 42, "static"]],
        [[#{"$ref" => "my_other"}, 7, "label"]]
    ],
    My_data.
