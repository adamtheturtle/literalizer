-module(fixture_literalize_ref_cpp_external_known_null_erlang_ref_default).
-export([x/0]).
x() ->
    Item = undefined,
    My_data = undefined,
    (void)my_data;
    My_data = Item,
    (void)my_data;.
