-module(fixture_literalize_ref_null_bound_list_hint_erlang_ref).
-export([x/0]).
x() ->
    My_value = undefined,
    My_data = My_value,
    My_data.
