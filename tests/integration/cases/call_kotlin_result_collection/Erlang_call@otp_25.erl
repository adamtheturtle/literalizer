-module(fixture_call_kotlin_result_collection_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget([[1, 2], [3]]),
    My_data.
