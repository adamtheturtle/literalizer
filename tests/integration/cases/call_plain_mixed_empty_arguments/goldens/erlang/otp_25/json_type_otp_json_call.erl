-module(fixture_call_plain_mixed_empty_arguments_erlang_json_type_otp_json_call).
-export([x/0]).
make_widget(_, _, _) -> undefined.
x() ->
    make_widget([], [1], []),
    make_widget([<<"text"/utf8>>], [2], []),
    make_widget([], [<<"text"/utf8>>], []),
    make_widget([<<"text"/utf8>>], [2], [3]).
