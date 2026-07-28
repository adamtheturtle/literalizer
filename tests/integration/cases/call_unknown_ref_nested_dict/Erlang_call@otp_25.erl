-module(fixture_call_unknown_ref_nested_dict_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    My_list = [],
    process([[#{"inner" => My_list}]]).
