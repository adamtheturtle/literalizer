-module(fixture_call_plain_nonempty_result_binding_erlang_collection_layout_compact_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget([1]),
    My_data.
