-module(fixture_literalize_ref_python_known_null_erlang_ref_default).
-export([x/0]).
x() ->
    Item = undefined,
    My_data = Item,
    My_data.
