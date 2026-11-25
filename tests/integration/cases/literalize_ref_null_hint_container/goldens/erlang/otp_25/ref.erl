-module(fixture_literalize_ref_null_hint_container_erlang_ref).
-export([x/0]).
x() ->
    My_value = [
        1,
        2
    ],
    My_data = My_value,
    My_data.
