-module(fixture_literalize_ref_cpp_external_known_null_erlang_ref_default).
-export([x/0]).
consume_widget(_) -> ok.
x() ->
    Item = undefined,
    My_data = undefined,
    consume_widget(My_data),
    My_data = Item,
    consume_widget(My_data).
