-module(fixture_call_ref_nested_in_list_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    My_var = 42,
    My_other = 7,
    process([#{"ref" => "my_var"}, 42, "static"]),
    process([#{"ref" => "my_other"}, 7, "label"]).
