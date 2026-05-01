-module(fixture_call_per_element_false_dict_arg_erlang_call).
-export([x/0]).
send(_) -> ok.
x() ->
    send(#{"a" => 1, "b" => "x"}).
