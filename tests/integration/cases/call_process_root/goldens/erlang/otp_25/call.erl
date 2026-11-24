-module(fixture_call_process_root_erlang_call).
-export([x/0]).
'process.api.fetch'(_) -> ok.
x() ->
    'process.api.fetch'(#{"data" => "hello"}),
    'process.api.fetch'(#{"data" => 42}),
    'process.api.fetch'(#{"data" => true}).
