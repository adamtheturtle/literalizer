-module(fixture_literalize_ref_cpp_external_empty_erlang_ref_default).
-export([x/0]).
x() ->
    Item = [
        1,
        2
    ],
    My_data = [
        1,
        2
    ],
    (void)my_data;
    My_data = Item,
    (void)my_data;.
