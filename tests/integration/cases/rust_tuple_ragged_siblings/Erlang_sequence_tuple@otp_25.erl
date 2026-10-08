-module(fixture_rust_tuple_ragged_siblings_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {"set_task", "web", "lint_web"},
        {"merge_pipelines"}
    },
    My_data.
