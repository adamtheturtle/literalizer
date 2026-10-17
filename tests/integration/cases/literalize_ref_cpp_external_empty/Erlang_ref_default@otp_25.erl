-module(fixture_literalize_ref_cpp_external_empty_erlang_ref_default).
-export([x/0]).
consume_widget(_) -> ok.
x() ->
    Item = [
        1,
        2
    ],
    My_data = [
        1,
        2
    ],
    consume_widget(My_data),
    My_data = Item,
    consume_widget(My_data).
