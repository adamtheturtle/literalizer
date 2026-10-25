-module(fixture_literalize_ref_external_repeated_opaque_list_erlang_ref_default).
-export([x/0]).
consume_widget(_) -> ok.
x() ->
    Item = [],
    My_data = [
        Item,
        Item
    ],
    consume_widget(My_data).
