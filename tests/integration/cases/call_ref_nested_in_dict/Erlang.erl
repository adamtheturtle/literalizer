-module(fixture_call_ref_nested_in_dict_erlang).
-export([x/0]).
x() ->
    My_data = [
        [#{"key" => #{"$ref" => "my_var"}, "count" => 42}]
    ],
    My_data.
