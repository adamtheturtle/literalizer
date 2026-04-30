-module(fixture_call_ref_args_reused_erlang).
-export([x/0]).
x() ->
    My_data = [
        [#{"$ref" => "repeated_var"}, 1],
        [#{"$ref" => "single_var"}, 0],
        [#{"$ref" => "repeated_var"}, 8]
    ],
    My_data.
