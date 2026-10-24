-module(fixture_sequence_ragged_siblings_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        ["set_task", "web", "lint_web"],
        ["merge_pipelines"]
    ],
    My_data.
