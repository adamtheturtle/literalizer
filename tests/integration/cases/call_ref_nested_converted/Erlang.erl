-module(fixture_call_ref_nested_converted_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[#{"$ref" => "myVar"}, 42, "static"]]
    ],
    My_data.
