-module(fixture_call_per_element_false_dict_arg_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(#{"a" => 1, "b" => "x"}).
