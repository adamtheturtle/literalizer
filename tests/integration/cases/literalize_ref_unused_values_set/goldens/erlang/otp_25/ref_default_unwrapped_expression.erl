-module(fixture_literalize_ref_unused_values_set_erlang_ref_default_unwrapped_expression).
-export([x/0]).
consume_widget(_) -> ok.
x() ->
    consume_widget(sets:from_list([
        1,
        2
    ])).
