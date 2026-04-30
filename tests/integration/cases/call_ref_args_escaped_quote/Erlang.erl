-module(fixture_call_ref_args_escaped_quote_erlang).
-export([x/0]).
x() ->
    My_data = [
        [#{"$ref" => "my_str"}]
    ],
    My_data.
