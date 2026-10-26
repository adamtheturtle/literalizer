-module(fixture_call_dotted_nested_empty_mapping_arguments_erlang_call).
-export([x/0]).
'api.worker.process'(_, _) -> ok.
x() ->
    'api.worker.process'([1, #{}], 42),
    'api.worker.process'([2, #{"x" => "s"}], 43).
