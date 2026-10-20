-module(fixture_literalize_ref_known_null_assignment_erlang_ref_default).
-export([x/0]).
x() ->
    Item = undefined,
    My_data = Item,
    My_data.
