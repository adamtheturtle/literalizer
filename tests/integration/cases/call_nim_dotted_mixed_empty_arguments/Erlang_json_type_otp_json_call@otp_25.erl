-module(fixture_call_nim_dotted_mixed_empty_arguments_erlang_json_type_otp_json_call).
-export([x/0]).
'thing.go'(_, _, _) -> undefined.
x() ->
    'thing.go'([], [1], []),
    'thing.go'([<<"text"/utf8>>], [2], []),
    'thing.go'([], [<<"text"/utf8>>], []),
    'thing.go'([<<"text"/utf8>>], [2], [3]).
