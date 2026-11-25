-module(fixture_literalize_ref_bound_boolean_erlang_ref).
-export([x/0]).
x() ->
    Ref_flag = true,
    My_data = Ref_flag,
    My_data.
