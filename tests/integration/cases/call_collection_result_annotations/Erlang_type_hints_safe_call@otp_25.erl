-module(fixture_call_collection_result_annotations_erlang_type_hints_safe_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget([[1, 2], [3]]),
    My_data.
