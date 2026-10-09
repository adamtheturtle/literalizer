-module(fixture_literalize_ref_gleam_scalar_list_hint_erlang_ref).
-export([x/0]).
x() ->
    Ref_data = 1,
    My_data = Ref_data,
    My_data.
